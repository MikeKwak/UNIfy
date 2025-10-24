"""
Hidden Markov Model (HMM) with Viterbi Processing for UNIfy
Models student journey through university application process and accommodation needs progression.
"""

import numpy as np
from hmmlearn import hmm
from typing import Dict, List, Tuple, Optional
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

class StudentJourneyHMM:
    """
    Hidden Markov Model for modeling student journey through university application process.
    
    States represent different stages:
    - Initial Assessment
    - Accommodation Planning
    - University Selection
    - Application Preparation
    - Final Recommendation
    
    Observations represent student characteristics and needs.
    """
    
    def __init__(self):
        """Initialize the HMM model."""
        # Define states in the student journey
        self.states = [
            'initial_assessment',      # State 0: Initial evaluation of student needs
            'accommodation_planning',  # State 1: Determining accommodations needed
            'university_selection',    # State 2: Selecting potential universities
            'application_prep',        # State 3: Preparing application strategy
            'final_recommendation'     # State 4: Final recommendations
        ]
        
        self.n_states = len(self.states)
        
        # Define observation symbols (discretized student features)
        self.observation_symbols = {
            'mental_health': ['None', 'ADHD', 'Autism', 'Depression', 'Anxiety', 'Other'],
            'physical_health': ['None', 'Hearing', 'Mobility', 'Vision', 'Neurological', 'Other'],
            'severity': ['mild', 'moderate', 'severe'],
            'gpa_level': ['low', 'medium', 'high', 'very_high'],
            'support_need': ['minimal', 'moderate', 'extensive']
        }
        
        # Initialize HMM with Gaussian emissions for continuous features
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the HMM with reasonable default parameters."""
        # Transition matrix: probability of moving from state i to state j
        # Students typically progress through states sequentially
        self.transition_matrix = np.array([
            # From: initial, accom_plan, uni_select, app_prep, final
            [0.1, 0.7, 0.1, 0.05, 0.05],  # initial_assessment -> mostly to accommodation_planning
            [0.05, 0.2, 0.6, 0.1, 0.05],  # accommodation_planning -> mostly to university_selection
            [0.05, 0.1, 0.3, 0.5, 0.05],  # university_selection -> mostly to application_prep
            [0.05, 0.05, 0.1, 0.3, 0.5],  # application_prep -> mostly to final_recommendation
            [0.05, 0.05, 0.05, 0.1, 0.75] # final_recommendation -> mostly stays in final
        ])
        
        # Initial state distribution - always start at initial assessment
        self.start_prob = np.array([0.8, 0.15, 0.03, 0.01, 0.01])
        
        # Create Gaussian HMM
        self.model = hmm.GaussianHMM(
            n_components=self.n_states,
            covariance_type="diag",
            n_iter=100,
            random_state=42
        )
        
        # Set the trained parameters
        self.model.startprob_ = self.start_prob
        self.model.transmat_ = self.transition_matrix
        
        # Initialize emission parameters (means and covariances for Gaussian emissions)
        # Features: [mental_health_encoded, physical_health_encoded, severity_encoded, gpa, support_complexity]
        n_features = 5
        
        # Mean values for each state
        self.model.means_ = np.array([
            [1.0, 1.0, 1.5, 3.0, 1.0],  # initial_assessment: moderate baseline
            [2.0, 1.5, 2.0, 3.0, 2.0],  # accommodation_planning: higher needs identified
            [2.5, 2.0, 2.0, 3.2, 2.5],  # university_selection: refined understanding
            [2.5, 2.0, 2.0, 3.2, 3.0],  # application_prep: detailed planning
            [2.5, 2.0, 2.0, 3.2, 3.0]   # final_recommendation: finalized
        ])
        
        # Covariance (variance) for each state
        self.model.covars_ = np.array([
            [1.5, 1.5, 0.5, 0.5, 1.0],  # initial_assessment: high variance (uncertain)
            [1.0, 1.0, 0.4, 0.4, 0.8],  # accommodation_planning: reducing uncertainty
            [0.8, 0.8, 0.3, 0.3, 0.6],  # university_selection: more certain
            [0.6, 0.6, 0.2, 0.2, 0.4],  # application_prep: very certain
            [0.5, 0.5, 0.1, 0.1, 0.3]   # final_recommendation: most certain
        ])
    
    def encode_student_profile(self, profile: Dict) -> np.ndarray:
        """
        Encode student profile into numerical features for HMM.
        
        Args:
            profile: Student profile dictionary
            
        Returns:
            Numpy array of encoded features
        """
        # Encode mental health
        mental_health = profile.get('mental_health', 'None')
        mental_health_map = {'None': 0, 'ADHD': 1, 'Autism': 2, 'Depression': 3, 'Anxiety': 4, 'Other': 5}
        mental_encoded = mental_health_map.get(mental_health, 0)
        
        # Encode physical health
        physical_health = profile.get('physical_health', 'None')
        physical_health_map = {'None': 0, 'Hearing': 1, 'Mobility': 2, 'Vision': 3, 'Neurological': 4, 'Other': 5}
        physical_encoded = physical_health_map.get(physical_health, 0)
        
        # Encode severity
        severity = profile.get('severity', 'moderate')
        severity_map = {'mild': 1, 'moderate': 2, 'severe': 3}
        severity_encoded = severity_map.get(severity, 2)
        
        # Normalize GPA to 0-4 scale
        gpa = float(profile.get('gpa', 3.0))
        
        # Calculate support complexity based on needs
        support_complexity = self._calculate_support_complexity(
            mental_encoded, physical_encoded, severity_encoded
        )
        
        return np.array([[mental_encoded, physical_encoded, severity_encoded, gpa, support_complexity]])
    
    def _calculate_support_complexity(self, mental: int, physical: int, severity: int) -> float:
        """Calculate how complex the support needs are."""
        # More conditions and higher severity = higher complexity
        complexity = 0.0
        
        if mental > 0:
            complexity += 1.0 + (severity - 1) * 0.5
        
        if physical > 0:
            complexity += 1.0 + (severity - 1) * 0.5
        
        # Both mental and physical = extra complexity
        if mental > 0 and physical > 0:
            complexity += 0.5
        
        return complexity
    
    def viterbi_decode(self, observations: np.ndarray) -> Tuple[List[str], List[float]]:
        """
        Use Viterbi algorithm to find the most likely sequence of states.
        
        Args:
            observations: Sequence of observations (student features over time or different aspects)
            
        Returns:
            Tuple of (state_sequence, probabilities)
        """
        # Run Viterbi algorithm
        log_prob, state_sequence = self.model.decode(observations, algorithm='viterbi')
        
        # Convert state indices to state names
        state_names = [self.states[idx] for idx in state_sequence]
        
        # Calculate state probabilities from log probability
        # Use the log probability and normalize it
        total_log_prob = log_prob / len(observations)  # Average log prob per observation
        confidence = np.exp(total_log_prob) if total_log_prob > -100 else 0.01
        
        # Create probability list (same confidence for all states in optimal path)
        state_probs = [confidence] * len(state_names)
        
        return state_names, state_probs
    
    def predict_journey_path(self, student_profile: Dict) -> Dict:
        """
        Predict the optimal journey path for a student using Viterbi algorithm.
        
        Args:
            student_profile: Student profile dictionary
            
        Returns:
            Dictionary with journey path and recommendations at each stage
        """
        # Encode student profile
        features = self.encode_student_profile(student_profile)
        
        # Create observation sequence (student profile at different decision points)
        # We model 5 observation points representing progression through process
        observation_sequence = self._create_observation_sequence(features, student_profile)
        
        # Use Viterbi to find optimal path
        state_path, state_probs = self.viterbi_decode(observation_sequence)
        
        # Generate recommendations for each state
        journey_map = self._create_journey_map(state_path, state_probs, student_profile)
        
        return journey_map
    
    def _create_observation_sequence(self, base_features: np.ndarray, profile: Dict) -> np.ndarray:
        """
        Create a sequence of observations representing student journey stages.
        
        As students progress, their understanding of needs becomes clearer,
        which we model as decreasing uncertainty in observations.
        """
        severity = profile.get('severity', 'moderate')
        severity_map = {'mild': 1, 'moderate': 2, 'severe': 3}
        severity_val = severity_map.get(severity, 2)
        
        # Create 5 observation points with progressively refined understanding
        sequence = []
        for i in range(5):
            # Add noise that decreases over time (uncertainty reduction)
            noise_scale = 1.0 - (i * 0.15)  # Decreases from 1.0 to 0.4
            
            # Copy base features and add controlled noise
            obs = base_features.copy()
            if i > 0:  # Add some variation to show progression
                noise = np.random.normal(0, noise_scale * 0.3, obs.shape)
                obs = obs + noise
                
                # Refine support complexity estimate over time
                obs[0, 4] = obs[0, 4] * (1 + i * 0.1)  # Support needs become clearer
            
            sequence.append(obs[0])
        
        return np.array(sequence)
    
    def _create_journey_map(self, state_path: List[str], state_probs: List[float], profile: Dict) -> Dict:
        """
        Create a comprehensive journey map with recommendations at each stage.
        
        Args:
            state_path: Sequence of states from Viterbi algorithm
            state_probs: Probabilities for each state
            profile: Student profile
            
        Returns:
            Dictionary with journey stages and recommendations
        """
        journey = {
            'optimal_path': state_path,
            'path_confidence': float(np.mean(state_probs)),
            'stages': [],
            'overall_recommendation': None
        }
        
        # Define actions for each state
        state_actions = {
            'initial_assessment': {
                'title': 'Initial Assessment',
                'description': 'Understanding your accessibility needs and academic goals',
                'actions': [
                    'Complete disability documentation',
                    'Identify primary accommodation needs',
                    'Set academic goals and preferences'
                ],
                'timeline': 'Month 1-2'
            },
            'accommodation_planning': {
                'title': 'Accommodation Planning',
                'description': 'Determining specific accommodations and support services needed',
                'actions': [
                    'Consult with accessibility advisors',
                    'Research accommodation types',
                    'Document specific needs for applications'
                ],
                'timeline': 'Month 2-3'
            },
            'university_selection': {
                'title': 'University Selection',
                'description': 'Identifying universities with best accessibility support',
                'actions': [
                    'Research university accessibility services',
                    'Compare accommodation availability',
                    'Visit campuses or attend virtual tours',
                    'Contact disability support offices'
                ],
                'timeline': 'Month 3-6'
            },
            'application_prep': {
                'title': 'Application Preparation',
                'description': 'Preparing applications highlighting your strengths and needs',
                'actions': [
                    'Prepare personal statements',
                    'Request accommodation letters',
                    'Gather required documentation',
                    'Complete application forms'
                ],
                'timeline': 'Month 6-8'
            },
            'final_recommendation': {
                'title': 'Final Recommendations',
                'description': 'Personalized university recommendations based on your needs',
                'actions': [
                    'Review top university matches',
                    'Compare accessibility ratings',
                    'Make informed decision',
                    'Submit applications'
                ],
                'timeline': 'Month 8-10'
            }
        }
        
        # Build journey stages
        for i, (state, prob) in enumerate(zip(state_path, state_probs)):
            if state in state_actions:
                stage_info = state_actions[state].copy()
                stage_info['stage_number'] = i + 1
                stage_info['confidence'] = float(prob)
                stage_info['status'] = 'current' if i == 0 else ('upcoming' if i < 3 else 'future')
                
                # Add state-specific recommendations based on profile
                stage_info['specific_recommendations'] = self._get_stage_recommendations(
                    state, profile
                )
                
                journey['stages'].append(stage_info)
        
        # Overall recommendation based on final state
        journey['overall_recommendation'] = self._generate_overall_recommendation(
            state_path, profile
        )
        
        return journey
    
    def _get_stage_recommendations(self, state: str, profile: Dict) -> List[str]:
        """Get specific recommendations for each stage based on student profile."""
        mental_health = profile.get('mental_health', 'None')
        physical_health = profile.get('physical_health', 'None')
        severity = profile.get('severity', 'moderate')
        
        recommendations = []
        
        if state == 'initial_assessment':
            if mental_health != 'None':
                recommendations.append(f'Document your {mental_health} diagnosis and history')
            if physical_health != 'None':
                recommendations.append(f'Gather medical documentation for {physical_health}')
            recommendations.append('List all current accommodations you use')
            
        elif state == 'accommodation_planning':
            if mental_health == 'ADHD':
                recommendations.extend([
                    'Consider extended time accommodations',
                    'Request quiet testing environments',
                    'Look into note-taking services'
                ])
            if mental_health == 'Autism':
                recommendations.extend([
                    'Research sensory-friendly spaces',
                    'Consider social skills support programs',
                    'Look for structured routine accommodations'
                ])
            if physical_health == 'Mobility':
                recommendations.extend([
                    'Prioritize wheelchair-accessible campuses',
                    'Research accessible housing options',
                    'Look for assistive technology support'
                ])
            if physical_health == 'Hearing':
                recommendations.extend([
                    'Research sign language interpreter availability',
                    'Look for captioning services',
                    'Consider hearing loop systems'
                ])
            if severity == 'severe':
                recommendations.append('Consider comprehensive support programs')
                
        elif state == 'university_selection':
            gpa = profile.get('gpa', 3.0)
            if gpa >= 3.7:
                recommendations.append('Consider highly competitive universities with strong disability support')
            elif gpa >= 3.0:
                recommendations.append('Focus on mid-tier universities with excellent accessibility services')
            else:
                recommendations.append('Look for universities with strong academic support and accessibility')
            
            recommendations.extend([
                'Compare disability support office ratings',
                'Review available accommodation types',
                'Check campus accessibility infrastructure'
            ])
            
        elif state == 'application_prep':
            recommendations.extend([
                'Write personal statement highlighting your strengths',
                'Explain how accommodations helped you succeed',
                'Request letters from accessibility advisors',
                'Prepare documentation package for each university'
            ])
            
        elif state == 'final_recommendation':
            recommendations.extend([
                'Apply to 5-8 universities with varying selectivity',
                'Ensure all have your required accommodations',
                'Submit early decision if confident about fit',
                'Follow up with disability services offices'
            ])
        
        return recommendations
    
    def _generate_overall_recommendation(self, state_path: List[str], profile: Dict) -> str:
        """Generate overall recommendation based on journey path."""
        mental_health = profile.get('mental_health', 'None')
        physical_health = profile.get('physical_health', 'None')
        severity = profile.get('severity', 'moderate')
        gpa = profile.get('gpa', 3.0)
        
        recommendation = f"Based on your profile ({mental_health} - {severity} severity, GPA: {gpa}), "
        
        # Determine recommended timeline
        if severity == 'severe' or (mental_health != 'None' and physical_health != 'None'):
            recommendation += "we recommend starting your university search 12-18 months before application deadlines. "
        elif severity == 'moderate':
            recommendation += "we recommend starting your university search 8-12 months before application deadlines. "
        else:
            recommendation += "we recommend starting your university search 6-8 months before application deadlines. "
        
        # Add specific focus areas
        focus_areas = []
        if mental_health != 'None':
            focus_areas.append('mental health support services')
        if physical_health != 'None':
            focus_areas.append('physical accessibility infrastructure')
        
        if focus_areas:
            recommendation += f"Focus on universities with strong {' and '.join(focus_areas)}. "
        
        # Add confidence note based on path
        if len(set(state_path)) >= 4:
            recommendation += "Your journey path shows comprehensive planning, which increases your chances of finding the perfect match."
        
        return recommendation
    
    def get_accommodation_progression(self, student_profile: Dict) -> Dict:
        """
        Model how accommodation needs might progress over time.
        
        Args:
            student_profile: Student profile dictionary
            
        Returns:
            Dictionary with accommodation progression recommendations
        """
        # Encode profile
        features = self.encode_student_profile(student_profile)
        
        # Predict likely states
        state_sequence, probs = self.viterbi_decode(
            self._create_observation_sequence(features, student_profile)
        )
        
        # Generate accommodation recommendations that evolve
        progression = {
            'immediate_needs': self._get_immediate_accommodations(student_profile),
            'semester_1_2': self._get_early_semester_accommodations(student_profile),
            'semester_3_4': self._get_mid_program_accommodations(student_profile),
            'upper_years': self._get_advanced_accommodations(student_profile),
            'confidence_score': float(np.mean(probs))
        }
        
        return progression
    
    def _get_immediate_accommodations(self, profile: Dict) -> List[str]:
        """Get accommodations needed immediately upon enrollment."""
        accommodations = ['Extended time on exams', 'Academic coaching']
        
        mental_health = profile.get('mental_health', 'None')
        physical_health = profile.get('physical_health', 'None')
        
        if mental_health == 'ADHD':
            accommodations.extend(['Quiet testing environment', 'Note-taking services'])
        if mental_health == 'Autism':
            accommodations.extend(['Structured schedule support', 'Social skills coaching'])
        if physical_health == 'Mobility':
            accommodations.extend(['Accessible classroom locations', 'Priority registration'])
        if physical_health == 'Hearing':
            accommodations.extend(['Sign language interpreters', 'Real-time captioning'])
        
        return accommodations
    
    def _get_early_semester_accommodations(self, profile: Dict) -> List[str]:
        """Get accommodations for early semesters (1-2)."""
        return [
            'Regular check-ins with disability advisor',
            'Academic skill development workshops',
            'Peer mentoring programs',
            'Technology orientation sessions'
        ]
    
    def _get_mid_program_accommodations(self, profile: Dict) -> List[str]:
        """Get accommodations for mid-program (semesters 3-4)."""
        return [
            'Research accommodation support',
            'Internship accessibility planning',
            'Advanced assistive technology',
            'Reduced course load options'
        ]
    
    def _get_advanced_accommodations(self, profile: Dict) -> List[str]:
        """Get accommodations for upper years."""
        return [
            'Thesis/capstone project accommodations',
            'Graduate school preparation support',
            'Career services accessibility',
            'Professional networking accommodations'
        ]
    
    def save_model(self, filepath: str = 'models/hmm_model.pkl'):
        """Save the HMM model to file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'states': self.states,
                'transition_matrix': self.transition_matrix,
                'start_prob': self.start_prob
            }, f)
        print(f"HMM model saved to {filepath}")
    
    def load_model(self, filepath: str = 'models/hmm_model.pkl') -> bool:
        """Load the HMM model from file."""
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.states = data['states']
                self.transition_matrix = data['transition_matrix']
                self.start_prob = data['start_prob']
            print(f"HMM model loaded from {filepath}")
            return True
        except Exception as e:
            print(f"Failed to load HMM model: {e}")
            return False


def get_hmm_enhanced_recommendations(student_profile: Dict) -> Dict:
    """
    Get HMM-enhanced recommendations using Viterbi algorithm.
    
    This provides:
    1. Optimal journey path through application process
    2. Stage-by-stage recommendations
    3. Accommodation progression over time
    
    Args:
        student_profile: Student profile dictionary
        
    Returns:
        Dictionary with HMM analysis and recommendations
    """
    hmm_model = StudentJourneyHMM()
    
    # Get optimal journey path using Viterbi
    journey_map = hmm_model.predict_journey_path(student_profile)
    
    # Get accommodation progression
    accommodation_progression = hmm_model.get_accommodation_progression(student_profile)
    
    # Combine results
    result = {
        'success': True,
        'analysis_type': 'hmm_viterbi',
        'journey_map': journey_map,
        'accommodation_progression': accommodation_progression,
        'viterbi_analysis': {
            'optimal_path': journey_map['optimal_path'],
            'path_confidence': journey_map['path_confidence'],
            'recommendation': journey_map['overall_recommendation']
        }
    }
    
    return result


if __name__ == "__main__":
    # Test the HMM system
    test_profile = {
        'mental_health': 'ADHD',
        'physical_health': 'None',
        'courses': 'Computer Science',
        'gpa': 3.8,
        'severity': 'moderate'
    }
    
    print("🧪 Testing HMM + Viterbi System")
    print("=" * 60)
    
    result = get_hmm_enhanced_recommendations(test_profile)
    
    print(f"\n✅ Success: {result['success']}")
    print(f"📊 Analysis Type: {result['analysis_type']}")
    print(f"\n🗺️ Optimal Journey Path (Viterbi):")
    for i, state in enumerate(result['viterbi_analysis']['optimal_path'], 1):
        print(f"  Stage {i}: {state}")
    
    print(f"\n💪 Path Confidence: {result['viterbi_analysis']['path_confidence']:.2%}")
    print(f"\n📋 Overall Recommendation:")
    print(f"  {result['viterbi_analysis']['recommendation']}")
    
    print(f"\n📅 Accommodation Progression:")
    prog = result['accommodation_progression']
    print(f"  Immediate Needs: {', '.join(prog['immediate_needs'][:3])}")
    print(f"  Early Semesters: {', '.join(prog['semester_1_2'][:2])}")
    print(f"  Confidence: {prog['confidence_score']:.2%}")
    
    print(f"\n🎯 Journey Stages ({len(result['journey_map']['stages'])} stages):")
    for stage in result['journey_map']['stages'][:3]:
        print(f"  • {stage['title']} ({stage['timeline']})")
        print(f"    - {stage['description']}")

