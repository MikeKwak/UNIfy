"""
Gemini AI Recommender for UNIfy
Provides AI-powered university accommodation recommendations.
"""

import os
import google.generativeai as genai
from typing import Dict, List, Optional
import json
import warnings
warnings.filterwarnings('ignore')


class GeminiRecommender:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini AI recommender.
        
        Args:
            api_key: Google AI API key. If None, will try to get from environment variable GEMINI_API_KEY
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("Warning: No Gemini API key provided. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
            self.available = False
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.available = True
            print("✅ Gemini AI recommender initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini AI: {str(e)}")
            self.available = False

    def get_recommendations(self, student_profile: Dict[str, any]) -> Dict[str, any]:
        """
        Get university recommendations using Gemini AI.
        
        Args:
            student_profile: Dictionary containing student information
            
        Returns:
            Dictionary with recommendations or error information
        """
        if not self.available:
            return {
                "success": False,
                "error": "Gemini AI not available. Please check API key configuration.",
                "source": "gemini_ai"
            }

        try:
            # Create a detailed prompt for Gemini
            prompt = self._create_prompt(student_profile)
            print(f"Generated prompt length: {len(prompt)} characters")
            
            # Get response from Gemini with timeout
            print("Calling Gemini API...")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2048,
                    temperature=0.3,  # Lower temperature for more consistent responses
                )
            )
            print("Received response from Gemini")
            
            # Check for safety issues before trying to access response.text
            if response.candidates and response.candidates[0].finish_reason == 2:
                print("Response blocked by safety filters (finish_reason=2)")
                # Try a much simpler approach
                try:
                    simple_prompt = f"List 3 Canadian universities good for {student_profile.get('courses', 'students')} students. Return as JSON with name, location, and reason fields."
                    simple_response = self.model.generate_content(simple_prompt)
                    if simple_response.text:
                        print("Simplified prompt succeeded")
                        recommendations = self._parse_gemini_response(simple_response.text)
                        return {
                            "success": True,
                            "source": "gemini_ai_simplified",
                            "needed_accommodations": recommendations.get("needed_accommodations", []),
                            "recommendations": recommendations.get("universities", [])
                        }
                except Exception as e:
                    print(f"Simplified prompt also failed: {e}")
                
                # Use fallback if simplified approach fails
                fallback = self._create_fallback_response("Response blocked by safety filters")
                return {
                    "success": True,
                    "source": "gemini_ai_fallback",
                    "needed_accommodations": fallback.get("needed_accommodations", []),
                    "recommendations": fallback.get("universities", [])
                }
            
            # Log raw response details
            print("=" * 50)
            print("RAW GEMINI RESPONSE DEBUG:")
            print("=" * 50)
            print(f"Response object type: {type(response)}")
            print(f"Response candidates: {len(response.candidates) if response.candidates else 0}")
            
            if response.candidates:
                for i, candidate in enumerate(response.candidates):
                    print(f"Candidate {i}:")
                    print(f"  Finish reason: {candidate.finish_reason}")
                    print(f"  Safety ratings: {candidate.safety_ratings}")
                    print(f"  Content parts: {len(candidate.content.parts) if candidate.content and candidate.content.parts else 0}")
                    if candidate.content and candidate.content.parts:
                        for j, part in enumerate(candidate.content.parts):
                            print(f"    Part {j}: {type(part)} - {part.text[:200] if hasattr(part, 'text') and part.text else 'No text'}")
            
            print(f"Response text: {response.text}")
            print(f"Response text length: {len(response.text) if response.text else 0}")
            print("=" * 50)
            
            # Check if response was blocked by safety filters
            if not response.text or not response.candidates:
                finish_reason = response.candidates[0].finish_reason if response.candidates else 'Unknown'
                print(f"Response blocked. Finish reason: {finish_reason}")
                
                # Map finish reasons to human-readable messages
                finish_reason_messages = {
                    0: "FINISH_REASON_UNSPECIFIED",
                    1: "STOP - Natural stop point",
                    2: "SAFETY - Blocked by safety filters", 
                    3: "RECITATION - Blocked due to recitation",
                    4: "OTHER - Other reason"
                }
                
                reason_msg = finish_reason_messages.get(finish_reason, f"Unknown reason ({finish_reason})")
                print(f"Blocked reason: {reason_msg}")
                
                # If blocked by safety filters, try a simpler approach
                if finish_reason == 2:  # SAFETY
                    print("Attempting with simplified prompt...")
                    try:
                        simple_prompt = f"""
                        Recommend 3 Canadian universities for a {student_profile.get('courses', 'student')} student with {student_profile.get('gpa', 3.0)} GPA.
                        Return as JSON: {{"universities": [{{"name": "University", "score": 4.0, "location": "Province", "reason": "Why suitable"}}]}}
                        """
                        simple_response = self.model.generate_content(simple_prompt)
                        if simple_response.text:
                            print("Simplified prompt succeeded")
                            recommendations = self._parse_gemini_response(simple_response.text)
                            return {
                                "success": True,
                                "source": "gemini_ai_simplified",
                                "needed_accommodations": recommendations.get("needed_accommodations", []),
                                "recommendations": recommendations.get("universities", [])
                            }
                    except Exception as e:
                        print(f"Simplified prompt also failed: {e}")
                
                # Use fallback if all attempts fail
                fallback = self._create_fallback_response(f"Response blocked: {reason_msg}")
                return {
                    "success": True,
                    "source": "gemini_ai_fallback",
                    "needed_accommodations": fallback.get("needed_accommodations", []),
                    "recommendations": fallback.get("universities", [])
                }
            
            # Parse the response
            print("Parsing Gemini response...")
            recommendations = self._parse_gemini_response(response.text)
            print(f"Parsed recommendations: {recommendations}")
            
            return {
                "success": True,
                "source": "gemini_ai",
                "needed_accommodations": recommendations.get("needed_accommodations", []),
                "recommendations": recommendations.get("universities", [])
            }
            
        except Exception as e:
            print(f"Error getting Gemini recommendations: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to get recommendations: {str(e)}",
                "source": "gemini_ai"
            }

    def _create_prompt(self, student_profile: Dict[str, any]) -> str:
        """Create a detailed prompt for Gemini AI."""
        # Create a more neutral prompt that avoids triggering safety filters
        academic_interests = student_profile.get('courses', 'General Studies')
        gpa = student_profile.get('gpa', 'Not specified')
        support_needs = []
        
        # Convert to more neutral language
        mental_health = student_profile.get('mental_health', 'None')
        physical_health = student_profile.get('physical_health', 'None')
        severity = student_profile.get('severity', 'Not specified')
        
        if mental_health != 'None':
            support_needs.append("academic support services")
        if physical_health != 'None':
            support_needs.append("accessibility services")
        
        support_description = ", ".join(support_needs) if support_needs else "standard academic support"
        
        return f"""
You are an educational counselor helping students find suitable universities in Canada.

Student Profile:
- Academic Field: {academic_interests}
- Academic Performance: {gpa} GPA
- Support Requirements: {support_description}
- Support Level: {severity}

Please provide university recommendations in this exact JSON format:

{{
  "needed_accommodations": ["accommodation1", "accommodation2", "accommodation3"],
  "universities": [
    {{
      "name": "University Name",
      "score": 4.5,
      "accessibility_rating": 4.3,
      "disability_support_rating": 4.7,
      "available_accommodations": ["accommodation1", "accommodation2"],
      "location": "Province/State",
      "reason": "Why this university is suitable for this student"
    }}
  ]
}}

Focus on:
1. Canadian universities with excellent academic programs in {academic_interests}
2. Universities with comprehensive student support services
3. Institutions known for accessibility and accommodation services
4. Academic quality and reputation
5. Practical reasons why each university would be suitable

Provide 3-5 university recommendations with detailed explanations.
"""

    def _parse_gemini_response(self, response_text: str) -> Dict[str, any]:
        """Parse Gemini's response and extract structured data."""
        print(f"Parsing response text (length: {len(response_text)}):")
        print(f"First 500 chars: {response_text[:500]}")
        print(f"Last 500 chars: {response_text[-500:]}")
        
        try:
            # Try to find JSON in the response - handle both object and array formats
            start_idx = response_text.find('{')
            array_start_idx = response_text.find('[')
            
            # Determine which format to use
            if array_start_idx != -1 and (start_idx == -1 or array_start_idx < start_idx):
                # Array format
                end_idx = response_text.rfind(']') + 1
                if end_idx != -1:
                    json_str = response_text[array_start_idx:end_idx]
                    print(f"Extracted JSON array (length: {len(json_str)}):")
                    print(f"JSON: {json_str}")
                    
                    universities_array = json.loads(json_str)
                    print(f"Successfully parsed JSON array: {universities_array}")
                    
                    # Convert array format to expected format
                    return {
                        "needed_accommodations": [
                            "Extended time for exams",
                            "Note-taking services", 
                            "Academic coaching",
                            "Priority registration"
                        ],
                        "universities": [
                            {
                                "name": uni.get("name", "Unknown University"),
                                "score": 4.0 + (hash(uni.get("name", "")) % 10) / 10,  # Generate score based on name
                                "accessibility_rating": 4.0 + (hash(uni.get("name", "")) % 10) / 10,
                                "disability_support_rating": 4.0 + (hash(uni.get("name", "")) % 10) / 10,
                                "available_accommodations": ["Extended time", "Note-taking services", "Academic coaching"],
                                "location": uni.get("location", "Unknown"),
                                "reason": uni.get("reason", "Good university for students")
                            }
                            for uni in universities_array
                        ]
                    }
            else:
                # Object format
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx]
                    print(f"Extracted JSON object (length: {len(json_str)}):")
                    print(f"JSON: {json_str}")
                    
                    parsed_json = json.loads(json_str)
                    print(f"Successfully parsed JSON object: {parsed_json}")
                    return parsed_json
            
            print("No valid JSON found in response, using fallback")
            # Fallback: create structured response from text
            return self._create_fallback_response(response_text)
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {str(e)}")
            print(f"Failed JSON string: {json_str if 'json_str' in locals() else 'N/A'}")
            # If JSON parsing fails, create a fallback response
            return self._create_fallback_response(response_text)

    def _create_fallback_response(self, response_text: str) -> Dict[str, any]:
        """Create a fallback response when JSON parsing fails."""
        return {
            "needed_accommodations": [
                "Extended time for exams",
                "Note-taking services",
                "Academic coaching",
                "Priority registration"
            ],
            "universities": [
                {
                    "name": "University of Toronto",
                    "score": 4.3,
                    "accessibility_rating": 4.5,
                    "disability_support_rating": 4.7,
                    "available_accommodations": ["Extended time", "Note-taking services", "Academic coaching"],
                    "location": "Ontario",
                    "reason": "Strong disability services and comprehensive support programs"
                },
                {
                    "name": "University of British Columbia",
                    "score": 4.1,
                    "accessibility_rating": 4.2,
                    "disability_support_rating": 4.4,
                    "available_accommodations": ["Extended time", "Alternative testing formats", "Assistive technology"],
                    "location": "British Columbia",
                    "reason": "Excellent accessibility infrastructure and support services"
                },
                {
                    "name": "McGill University",
                    "score": 3.9,
                    "accessibility_rating": 4.0,
                    "disability_support_rating": 4.1,
                    "available_accommodations": ["Extended time", "Note-taking services", "Priority registration"],
                    "location": "Quebec",
                    "reason": "Comprehensive disability support and accommodation services"
                }
            ]
        }


# Global instance
_gemini_recommender = None

def get_gemini_recommendations(student_profile: Dict[str, any]) -> Dict[str, any]:
    """
    Get recommendations from Gemini AI.
    
    Args:
        student_profile: Dictionary containing student information
        
    Returns:
        Dictionary with recommendations or error information
    """
    global _gemini_recommender
    
    if _gemini_recommender is None:
        _gemini_recommender = GeminiRecommender()
    
    return _gemini_recommender.get_recommendations(student_profile)
