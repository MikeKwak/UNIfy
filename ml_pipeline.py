"""
UNIfy Machine Learning Pipeline
Builds a recommendation system to match students with disabilities to universities
based on available accommodations using TensorFlow.
"""

import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.metrics import classification_report, accuracy_score
import pickle
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class UNIfyMLPipeline:
    def __init__(self, data_dir: str = "data/clean"):
        """
        Initialize the UNIfy ML Pipeline.
        
        Args:
            data_dir: Directory containing cleaned CSV files
        """
        self.data_dir = data_dir
        self.student_data = None
        self.university_data = None
        self.user_input_data = None
        
        # ML components
        self.disability_encoder = LabelEncoder()
        self.course_encoder = LabelEncoder()
        self.accommodation_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        
        # Models
        self.accommodation_predictor = None
        self.university_recommender = None
        
        # Data mappings
        self.disability_mapping = {}
        self.course_mapping = {}
        self.accommodation_mapping = {}
        
    def load_data(self):
        """Load and preprocess the cleaned CSV files."""
        print("Loading cleaned data...")
        
        # Load student info
        self.student_data = pd.read_csv(os.path.join(self.data_dir, "clean_student_info.csv"))
        print(f"Loaded student data: {self.student_data.shape}")
        
        # Load university info (handle large file)
        try:
            self.university_data = pd.read_csv(os.path.join(self.data_dir, "clean_uni_info.csv"))
            print(f"Loaded university data: {self.university_data.shape}")
        except Exception as e:
            print(f"Warning: Could not load university data: {e}")
            # Create sample university data for demonstration
            self._create_sample_university_data()
        
        # Load user input
        self.user_input_data = pd.read_csv(os.path.join(self.data_dir, "clean_user_input.csv"))
        print(f"Loaded user input data: {self.user_input_data.shape}")
        
        return self
    
    def _create_sample_university_data(self):
        """Create sample university data for demonstration purposes."""
        universities = [
            "University of Toronto", "McGill University", "University of British Columbia",
            "University of Alberta", "University of Waterloo", "University of Ottawa",
            "Queen's University", "Western University", "University of Calgary",
            "University of Montreal"
        ]
        
        accommodations = [
            "Note-taking services", "Extended time on exams", "Quiet testing environment",
            "Accessible housing", "Sign language interpreters", "Assistive technology",
            "Academic coaching", "Flexible attendance", "Alternative format materials",
            "Campus accessibility", "Mental health support", "Physical therapy services"
        ]
        
        # Create sample data
        sample_data = []
        for i, uni in enumerate(universities):
            # Randomly assign accommodations
            num_accommodations = np.random.randint(5, 12)
            uni_accommodations = np.random.choice(accommodations, num_accommodations, replace=False)
            
            sample_data.append({
                'university_id': i + 1,
                'university_name': uni,
                'available_accommodations': ';'.join(uni_accommodations),
                'accessibility_rating': np.random.uniform(3.5, 5.0),
                'disability_support_rating': np.random.uniform(3.5, 5.0)
            })
        
        self.university_data = pd.DataFrame(sample_data)
        print("Created sample university data for demonstration")
    
    def preprocess_student_data(self):
        """Preprocess student disability and course data."""
        print("Preprocessing student data...")
        
        # Clean disability columns
        disability_cols = ['mental_health_conditions', 'physical_health_conditions']
        for col in disability_cols:
            if col in self.student_data.columns:
                # Handle missing values and standardize
                self.student_data[col] = self.student_data[col].fillna('None')
                self.student_data[col] = self.student_data[col].str.replace('Types', 'ADHD')
                self.student_data[col] = self.student_data[col].str.replace('Severity', 'ADHD')
        
        # Clean course data
        if 'list_of_high_school_courses' in self.student_data.columns:
            self.student_data['list_of_high_school_courses'] = \
                self.student_data['list_of_high_school_courses'].fillna('None')
        
        return self
    
    def preprocess_user_input(self):
        """Preprocess user input data for ML training."""
        print("Preprocessing user input data...")
        
        # Clean health condition data
        if 'health_condition' in self.user_input_data.columns:
            self.user_input_data['health_condition'] = \
                self.user_input_data['health_condition'].fillna('None')
            # Remove angle brackets and clean up
            self.user_input_data['health_condition'] = \
                self.user_input_data['health_condition'].str.replace('<', '').str.replace('>', '')
        
        # Clean severity data
        if 'severity' in self.user_input_data.columns:
            self.user_input_data['severity'] = \
                self.user_input_data['severity'].fillna('moderate')
        
        # Clean GPA data
        if 'gpa' in self.user_input_data.columns:
            # Extract numeric GPA values
            self.user_input_data['gpa_numeric'] = \
                self.user_input_data['gpa'].str.extract(r'(\d+\.?\d*)').astype(float)
            self.user_input_data['gpa_numeric'] = \
                self.user_input_data['gpa_numeric'].fillna(3.0)  # Default to 3.0
        
        return self
    
    def create_training_data(self):
        """Create training data for the ML models."""
        print("Creating training data...")
        
        # Create minimal training data for quick testing
        if self.student_data is not None and self.user_input_data is not None:
            # Use only a tiny subset for quick testing
            max_training_examples = 100  # Drastically reduced for speed
            
            # Take minimal samples
            student_sample = self.student_data.sample(n=min(10, len(self.student_data)), random_state=42)
            user_sample = self.user_input_data.sample(n=min(10, len(self.user_input_data)), random_state=42)
            
            print(f"Using {len(student_sample)} student profiles and {len(user_sample)} user inputs")
            
            training_data = []
            for _, student_row in student_sample.iterrows():
                for _, user_row in user_sample.iterrows():
                    # Create a training example
                    training_example = {
                        'student_id': student_row.get('student_info_id', 0),
                        'mental_health': student_row.get('mental_health_conditions', 'None'),
                        'physical_health': student_row.get('physical_health_conditions', 'None'),
                        'courses': student_row.get('list_of_high_school_courses', 'None'),
                        'gpa': user_row.get('gpa_numeric', 3.0),
                        'health_condition': user_row.get('health_condition', 'None'),
                        'severity': user_row.get('severity', 'moderate'),
                        'extracurriculars': user_row.get('list_of_extracurricular_activities', 'None')
                    }
                    training_data.append(training_example)
                    
                    # Limit total training examples
                    if len(training_data) >= max_training_examples:
                        break
                if len(training_data) >= max_training_examples:
                    break
            
            self.training_data = pd.DataFrame(training_data)
            print(f"Created training data: {self.training_data.shape}")
            print(f"Training examples limited to {max_training_examples} for quick testing")
        
        return self
    
    def encode_categorical_features(self):
        """Encode categorical features for ML training."""
        print("Encoding categorical features...")
        
        if not hasattr(self, 'training_data'):
            print("No training data available. Run create_training_data() first.")
            return self
        
        # Encode mental health conditions
        if 'mental_health' in self.training_data.columns:
            self.training_data['mental_health_encoded'] = \
                self.disability_encoder.fit_transform(self.training_data['mental_health'])
        
        # Encode physical health conditions
        if 'physical_health' in self.training_data.columns:
            self.training_data['physical_health_encoded'] = \
                self.disability_encoder.transform(self.training_data['physical_health'])
        
        # Encode courses
        if 'courses' in self.training_data.columns:
            self.training_data['courses_encoded'] = \
                self.course_encoder.fit_transform(self.training_data['courses'])
        
        # Encode health conditions
        if 'health_condition' in self.training_data.columns:
            self.training_data['health_condition_encoded'] = \
                self.disability_encoder.transform(self.training_data['health_condition'])
        
        # Encode severity (ordinal)
        severity_mapping = {'mild': 1, 'moderate': 2, 'severe': 3}
        if 'severity' in self.training_data.columns:
            self.training_data['severity_encoded'] = \
                self.training_data['severity'].map(severity_mapping).fillna(2)
        
        return self
    
    def build_accommodation_predictor(self):
        """Build a neural network to predict needed accommodations."""
        print("Building accommodation predictor model...")
        
        # Prepare features
        feature_cols = [
            'mental_health_encoded', 'physical_health_encoded', 'courses_encoded',
            'gpa_numeric', 'health_condition_encoded', 'severity_encoded'
        ]
        
        if not all(col in self.training_data.columns for col in feature_cols):
            print("Missing required features. Run encode_categorical_features() first.")
            return self
        
        X = self.training_data[feature_cols].values
        X = self.scaler.fit_transform(X)
        
        # Create synthetic accommodation labels (for demonstration)
        # In real implementation, this would come from actual accommodation data
        accommodation_labels = []
        for _, row in self.training_data.iterrows():
            accommodations = []
            if row['mental_health'] != 'None':
                accommodations.extend(['Extended time', 'Quiet environment', 'Academic coaching'])
            if row['physical_health'] != 'None':
                accommodations.extend(['Accessible facilities', 'Assistive technology'])
            if row['severity'] == 'severe':
                accommodations.append('Personal assistant')
            
            accommodation_labels.append(accommodations)
        
        # Encode accommodation labels
        mlb = MultiLabelBinarizer()
        y = mlb.fit_transform(accommodation_labels)
        self.accommodation_mapping = {i: label for i, label in enumerate(mlb.classes_)}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Build model - simplified for quick testing
        self.accommodation_predictor = keras.Sequential([
            layers.Dense(32, activation='relu', input_shape=(X.shape[1],)),  # Reduced from 128
            layers.Dropout(0.2),  # Reduced from 0.3
            layers.Dense(16, activation='relu'),  # Reduced from 64
            layers.Dense(y.shape[1], activation='sigmoid')
        ])
        
        self.accommodation_predictor.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Add early stopping to prevent overfitting and reduce training time
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=3,  # Reduced from 5
            restore_best_weights=True,
            verbose=1
        )
        
        # Train model with minimal epochs for quick testing
        print("Training accommodation predictor...")
        history = self.accommodation_predictor.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=5,  # Drastically reduced from 20 to 5
            batch_size=16,  # Reduced from 32
            callbacks=[early_stopping],
            verbose=1
        )
        
        # Evaluate
        y_pred = self.accommodation_predictor.predict(X_test)
        y_pred_binary = (y_pred > 0.5).astype(int)
        
        print("\nAccommodation Predictor Results:")
        print(f"Accuracy: {accuracy_score(y_test, y_pred_binary):.4f}")
        
        return self
    
    def build_university_recommender(self):
        """Build a recommendation system for universities."""
        print("Building university recommender...")
        
        if self.university_data is None:
            print("No university data available.")
            return self
        
        # Create university embeddings
        university_features = []
        university_names = []
        
        for _, uni_row in self.university_data.iterrows():
            # Extract accommodation features
            accommodations = uni_row.get('available_accommodations', '').split(';')
            
            # Create feature vector
            features = []
            features.append(uni_row.get('accessibility_rating', 3.5))
            features.append(uni_row.get('disability_support_rating', 3.5))
            
            # Add accommodation indicators
            all_accommodations = [
                'Note-taking services', 'Extended time', 'Quiet environment',
                'Accessible housing', 'Sign language interpreters', 'Assistive technology',
                'Academic coaching', 'Flexible attendance', 'Alternative format materials',
                'Campus accessibility', 'Mental health support', 'Physical therapy services'
            ]
            
            for acc in all_accommodations:
                features.append(1.0 if acc in accommodations else 0.0)
            
            university_features.append(features)
            university_names.append(uni_row.get('university_name', 'Unknown'))
        
        self.university_features = np.array(university_features)
        self.university_names = university_names
        
        # Build recommendation model - simplified for quick testing
        self.university_recommender = keras.Sequential([
            layers.Dense(16, activation='relu', input_shape=(self.university_features.shape[1],)),  # Reduced from 64
            layers.Dropout(0.1),  # Reduced from 0.2
            layers.Dense(8, activation='relu'),  # Reduced from 32
            layers.Dense(1, activation='linear')
        ])
        
        self.university_recommender.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        print("University recommender built successfully!")
        return self
    
    def recommend_universities(self, student_profile: Dict) -> List[Tuple[str, float]]:
        """
        Recommend universities for a given student profile.
        
        Args:
            student_profile: Dictionary containing student information
            
        Returns:
            List of (university_name, score) tuples
        """
        if self.university_recommender is None:
            print("University recommender not built. Run build_university_recommender() first.")
            return []
        
        # Predict accommodations needed
        if self.accommodation_predictor is not None:
            # Encode student profile
            features = self._encode_student_profile(student_profile)
            features_scaled = self.scaler.transform([features])
            
            # Predict accommodations
            accommodation_pred = self.accommodation_predictor.predict(features_scaled)[0]
            needed_accommodations = [
                self.accommodation_mapping[i] for i, pred in enumerate(accommodation_pred) 
                if pred > 0.5
            ]
            print(f"Predicted accommodations needed: {needed_accommodations}")
        
        # Score universities based on accommodation match
        university_scores = []
        for i, uni_name in enumerate(self.university_names):
            score = self._calculate_university_score(i, needed_accommodations)
            university_scores.append((uni_name, score))
        
        # Sort by score (descending)
        university_scores.sort(key=lambda x: x[1], reverse=True)
        
        return university_scores[:5]  # Return top 5 recommendations
    
    def _encode_student_profile(self, profile: Dict) -> np.ndarray:
        """Encode a student profile into feature vector."""
        features = []
        
        # Encode mental health
        mental_health = profile.get('mental_health', 'None')
        features.append(self.disability_encoder.transform([mental_health])[0])
        
        # Encode physical health
        physical_health = profile.get('physical_health', 'None')
        features.append(self.disability_encoder.transform([physical_health])[0])
        
        # Encode courses
        courses = profile.get('courses', 'None')
        features.append(self.course_encoder.transform([courses])[0])
        
        # Add other features
        features.append(profile.get('gpa', 3.0))
        features.append(profile.get('severity_encoded', 2))
        
        return np.array(features)
    
    def _calculate_university_score(self, uni_idx: int, needed_accommodations: List[str]) -> float:
        """Calculate how well a university matches student needs."""
        if not hasattr(self, 'university_features'):
            return 0.0
        
        uni_features = self.university_features[uni_idx]
        
        # Base score from ratings
        base_score = (uni_features[0] + uni_features[1]) / 2  # Average of accessibility and support ratings
        
        # Accommodation match score
        accommodation_score = 0.0
        if needed_accommodations:
            # Check which accommodations are available (features[2:] are accommodation indicators)
            available_accommodations = []
            all_accommodations = [
                'Note-taking services', 'Extended time', 'Quiet environment',
                'Accessible housing', 'Sign language interpreters', 'Assistive technology',
                'Academic coaching', 'Flexible attendance', 'Alternative format materials',
                'Campus accessibility', 'Mental health support', 'Physical therapy services'
            ]
            
            for i, acc in enumerate(all_accommodations):
                if uni_features[2 + i] > 0.5:  # Accommodation is available
                    available_accommodations.append(acc)
            
            # Calculate match percentage
            matches = sum(1 for acc in needed_accommodations if acc in available_accommodations)
            accommodation_score = matches / len(needed_accommodations) if needed_accommodations else 0.0
        
        # Combine scores
        final_score = 0.7 * base_score + 0.3 * accommodation_score
        return final_score
    
    def save_models(self, output_dir: str = "models"):
        """Save trained models and encoders."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save accommodation predictor
        if self.accommodation_predictor:
            self.accommodation_predictor.save(os.path.join(output_dir, 'accommodation_predictor.h5'))
            print(f"Saved accommodation predictor to {output_dir}/accommodation_predictor.h5")
        
        # Save university recommender
        if self.university_recommender:
            self.university_recommender.save(os.path.join(output_dir, 'university_recommender.h5'))
            print(f"Saved university recommender to {output_dir}/university_recommender.h5")
        
        # Save encoders and scalers
        with open(os.path.join(output_dir, 'encoders.pkl'), 'wb') as f:
            pickle.dump({
                'disability_encoder': self.disability_encoder,
                'course_encoder': self.course_encoder,
                'accommodation_encoder': self.accommodation_encoder,
                'scaler': self.scaler,
                'accommodation_mapping': self.accommodation_mapping
            }, f)
        
        print(f"Saved encoders to {output_dir}/encoders.pkl")
        
        return self
    
    def run_full_pipeline(self):
        """Run the complete ML pipeline."""
        print("Starting UNIfy ML Pipeline...")
        
        (self.load_data()
             .preprocess_student_data()
             .preprocess_user_input()
             .create_training_data()
             .encode_categorical_features()
             .build_accommodation_predictor()
             .build_university_recommender()
             .save_models())
        
        print("UNIfy ML Pipeline completed successfully!")
        return self


# API Functions for Frontend Integration
def get_recommendations(student_profile: Dict) -> Dict:
    """
    Main API function for frontend integration.
    
    Args:
        student_profile: Dictionary with keys:
            - mental_health: str (e.g., 'ADHD', 'Autism', 'None')
            - physical_health: str (e.g., 'Hearing', 'Mobility', 'None')
            - courses: str (e.g., 'Computer Science', 'Mathematics')
            - gpa: float (e.g., 3.8)
            - severity: str (e.g., 'mild', 'moderate', 'severe')
    
    Returns:
        Dictionary with:
            - success: bool
            - needed_accommodations: List[str]
            - recommendations: List[Dict] with university info
    """
    try:
        # Load trained models
        pipeline = UNIfyMLPipeline()
        
        # Check if models exist, if not train them
        if not os.path.exists('models/encoders.pkl'):
            print("Models not found. Training new models...")
            pipeline.run_full_pipeline()
        else:
            # Load existing models
            pipeline.load_data()
            pipeline.preprocess_student_data()
            pipeline.preprocess_user_input()
            pipeline.create_training_data()
            pipeline.encode_categorical_features()
            
            # Load saved models
            with open('models/encoders.pkl', 'rb') as f:
                encoders = pickle.load(f)
                pipeline.disability_encoder = encoders['disability_encoder']
                pipeline.course_encoder = encoders['course_encoder']
                pipeline.scaler = encoders['scaler']
                pipeline.accommodation_mapping = encoders['accommodation_mapping']
            
            if os.path.exists('models/accommodation_predictor.h5'):
                pipeline.accommodation_predictor = keras.models.load_model('models/accommodation_predictor.h5')
            
            if os.path.exists('models/university_recommender.h5'):
                pipeline.university_recommender = keras.models.load_model('models/university_recommender.h5')
        
        # Get recommendations
        recommendations = pipeline.recommend_universities(student_profile)
        
        # Format response for frontend
        formatted_recommendations = []
        for uni_name, score in recommendations:
            # Find university details
            uni_data = pipeline.university_data[pipeline.university_data['university_name'] == uni_name]
            if not uni_data.empty:
                uni_row = uni_data.iloc[0]
                available_acc = uni_row.get('available_accommodations', '').split(';')
                
                formatted_recommendations.append({
                    'name': uni_name,
                    'score': round(score, 3),
                    'accessibility_rating': round(uni_row.get('accessibility_rating', 3.5), 1),
                    'disability_support_rating': round(uni_row.get('disability_support_rating', 3.5), 1),
                    'available_accommodations': available_acc,
                    'location': 'Unknown'  # Add if available in your data
                })
        
        return {
            'success': True,
            'needed_accommodations': ['Extended time', 'Quiet environment', 'Academic coaching'],  # Placeholder
            'recommendations': formatted_recommendations
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'recommendations': []
        }


def main():
    """Main function to run the pipeline."""
    # Initialize pipeline
    pipeline = UNIfyMLPipeline()
    
    # Run full pipeline
    pipeline.run_full_pipeline()
    
    # Test recommendation system
    print("\n" + "="*50)
    print("TESTING RECOMMENDATION SYSTEM")
    print("="*50)
    
    # Test student profile
    test_profile = {
        'mental_health': 'ADHD',
        'physical_health': 'None',
        'courses': 'Computer Science',
        'gpa': 3.8,
        'severity': 'moderate'
    }
    
    recommendations = pipeline.recommend_universities(test_profile)
    
    print(f"\nRecommendations for student with {test_profile['mental_health']}:")
    for i, (uni, score) in enumerate(recommendations, 1):
        print(f"{i}. {uni} (Score: {score:.3f})")
    
    # Test API function
    print("\n" + "="*50)
    print("TESTING API FUNCTION")
    print("="*50)
    
    api_result = get_recommendations(test_profile)
    if api_result['success']:
        print("API function working correctly!")
        print(f"Found {len(api_result['recommendations'])} recommendations")
    else:
        print(f"API function error: {api_result['error']}")


if __name__ == "__main__":
    main()
