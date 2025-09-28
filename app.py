"""
UNIfy Flask API Server
Provides REST API endpoints for the React frontend to access ML/AI recommendations.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from typing import Dict, Any

# Import our ML/AI systems
from ml_pipeline import get_recommendations
try:
    from gemini_recommender import get_gemini_recommendations
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'UNIfy API server is running',
        'version': '1.0.0',
        'endpoints': {
            'recommendations': '/api/recommendations',
            'health': '/',
            'test': '/api/test'
        }
    })

@app.route('/api/recommendations', methods=['POST'])
def get_university_recommendations():
    """
    Main API endpoint for getting university recommendations.
    
    Expected JSON payload:
    {
        "mental_health": "ADHD",
        "physical_health": "None", 
        "courses": "Computer Science",
        "gpa": 3.8,
        "severity": "moderate"
    }
    
    Returns:
    {
        "success": true,
        "source": "ml_pipeline|gemini_ai|default_fallback",
        "needed_accommodations": ["Extended time", "Academic coaching"],
        "recommendations": [
            {
                "name": "University of Toronto",
                "score": 4.3,
                "accessibility_rating": 4.5,
                "disability_support_rating": 4.7,
                "available_accommodations": ["Extended time", "Note-taking services"],
                "location": "Ontario",
                "reason": "Strong disability services"
            }
        ]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['mental_health', 'physical_health', 'courses', 'gpa', 'severity']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate data types and ranges
        try:
            gpa = float(data['gpa'])
            if not 0.0 <= gpa <= 4.0:
                return jsonify({
                    'success': False,
                    'error': 'GPA must be between 0.0 and 4.0'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'GPA must be a valid number'
            }), 400
        
        # Validate severity
        valid_severities = ['mild', 'moderate', 'severe']
        if data['severity'] not in valid_severities:
            return jsonify({
                'success': False,
                'error': f'Severity must be one of: {", ".join(valid_severities)}'
            }), 400
        
        # Create student profile
        student_profile = {
            'mental_health': str(data['mental_health']),
            'physical_health': str(data['physical_health']),
            'courses': str(data['courses']),
            'gpa': gpa,
            'severity': str(data['severity'])
        }
        
        logger.info(f"Processing recommendation request for: {student_profile}")
        
        # Get recommendations from ML/AI pipeline
        result = get_recommendations(student_profile)
        
        logger.info(f"Recommendation result: success={result['success']}, source={result.get('source', 'unknown')}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in recommendations endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_recommendations():
    """Test endpoint with sample data."""
    try:
        # Sample student profile for testing
        test_profile = {
            'mental_health': 'ADHD',
            'physical_health': 'None',
            'courses': 'Computer Science',
            'gpa': 3.8,
            'severity': 'moderate'
        }
        
        logger.info("Running test recommendation")
        result = get_recommendations(test_profile)
        
        return jsonify({
            'message': 'Test completed successfully',
            'test_profile': test_profile,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gemini', methods=['POST'])
def get_gemini_recommendations_endpoint():
    """
    Direct Gemini AI endpoint for testing.
    
    Expected JSON payload: same as /api/recommendations
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        
        # Create student profile (same validation as main endpoint)
        required_fields = ['mental_health', 'physical_health', 'courses', 'gpa', 'severity']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        student_profile = {
            'mental_health': str(data['mental_health']),
            'physical_health': str(data['physical_health']),
            'courses': str(data['courses']),
            'gpa': float(data['gpa']),
            'severity': str(data['severity'])
        }
        
        logger.info(f"Processing Gemini AI request for: {student_profile}")
        
        # Get recommendations directly from Gemini AI
        result = get_gemini_recommendations(student_profile)
        
        logger.info(f"Gemini AI result: success={result['success']}, source={result.get('source', 'unknown')}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in Gemini endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': ['/', '/api/recommendations', '/api/test', '/api/gemini']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

def create_app():
    """Application factory pattern."""
    return app



@app.route('/api/recommendations/verify', methods=['POST'])
def verify_recommendations_with_llm():
    """
    Enhanced endpoint that combines ML pipeline results with Gemini AI verification
    """
    try:
        data = request.get_json()
        student_profile = {
            'mental_health': str(data.get('mental_health', 'None')),
            'physical_health': str(data.get('physical_health', 'None')),
            'courses': str(data.get('courses', 'General Studies')),
            'gpa': float(data.get('gpa', 3.0)),
            'severity': str(data.get('severity', 'moderate'))
        }
        
        logger.info(f"Verification request for profile: {student_profile}")
        
        # Step 1: Get ML pipeline results (either provided or generate fresh)
        initial_results = data.get('initial_results')
        if not initial_results or not initial_results.get('recommendations'):
            logger.info("Getting fresh ML recommendations...")
            initial_results = get_recommendations(student_profile)
        
        # Step 2: Get Gemini AI verification/enhancement
        logger.info("Getting Gemini AI verification...")
        if GEMINI_AVAILABLE:
            try:
                gemini_verification = get_gemini_recommendations(student_profile)
            except Exception as e:
                logger.warning(f"Gemini AI failed, using ML results only: {e}")
                gemini_verification = None
        else:
            logger.warning("Gemini AI not available")
            gemini_verification = None
        
        # Step 3: Combine and verify results
        verified_results = combine_and_verify_results(initial_results, gemini_verification)
        
        logger.info(f"Verification complete: {verified_results.get('source', 'unknown')}")
        return jsonify(verified_results)
        
    except Exception as e:
        logger.error(f"Error in verification endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate verified recommendations',
            'details': str(e)
        }), 500


def combine_and_verify_results(ml_results, gemini_results):
    """
    Intelligent combination of ML and Gemini results with confidence scoring
    """
    if not ml_results.get('success'):
        # If ML failed, try to use Gemini results
        if gemini_results and gemini_results.get('success'):
            gemini_results['source'] = 'gemini_fallback'
            return gemini_results
        else:
            return {
                'success': False,
                'error': 'Both ML and AI systems failed to generate recommendations'
            }
    
    if not gemini_results or not gemini_results.get('success'):
        # If Gemini failed, use ML results only
        ml_results['source'] = 'ml_only'
        ml_results['verification_note'] = 'LLM verification unavailable, using ML results only'
        return ml_results
    
    # Both systems succeeded - combine intelligently
    
    # Combine accommodations with deduplication
    ml_accommodations = set(ml_results.get('needed_accommodations', []))
    gemini_accommodations = set(gemini_results.get('needed_accommodations', []))
    combined_accommodations = list(ml_accommodations.union(gemini_accommodations))
    
    # Process universities from both systems
    ml_unis = {uni['name']: uni for uni in ml_results.get('recommendations', [])}
    gemini_unis = {uni['name']: uni for uni in gemini_results.get('recommendations', [])}
    
    combined_recommendations = []
    
    # High confidence: Universities recommended by both systems
    overlap_unis = set(ml_unis.keys()).intersection(set(gemini_unis.keys()))
    for name in overlap_unis:
        ml_uni = ml_unis[name]
        gemini_uni = gemini_unis[name]
        
        combined_recommendations.append({
            'name': name,
            'score': round((ml_uni.get('score', 0) + gemini_uni.get('score', 0)) / 2, 3),
            'confidence': 'high',
            'ml_score': ml_uni.get('score', 0),
            'ai_score': gemini_uni.get('score', 0),
            'accessibility_rating': max(
                ml_uni.get('accessibility_rating', 0), 
                gemini_uni.get('accessibility_rating', 0)
            ),
            'disability_support_rating': max(
                ml_uni.get('disability_support_rating', 0), 
                gemini_uni.get('disability_support_rating', 0)
            ),
            'available_accommodations': list(set(
                ml_uni.get('available_accommodations', []) + 
                gemini_uni.get('available_accommodations', [])
            )),
            'location': ml_uni.get('location') or gemini_uni.get('location', 'Unknown'),
            'reason': f"Both ML and AI systems recommend this university. {ml_uni.get('reason', '')}",
            'source': 'both_systems'
        })
    
    # Medium confidence: Unique ML recommendations
    ml_only_unis = set(ml_unis.keys()) - set(gemini_unis.keys())
    for name in ml_only_unis:
        uni = ml_unis[name].copy()
        uni['confidence'] = 'medium'
        uni['source'] = 'ml_only'
        uni['reason'] = f"ML recommendation: {uni.get('reason', '')}"
        combined_recommendations.append(uni)
    
    # Medium confidence: Unique Gemini recommendations
    gemini_only_unis = set(gemini_unis.keys()) - set(ml_unis.keys())
    for name in gemini_only_unis:
        uni = gemini_unis[name].copy()
        uni['confidence'] = 'medium'
        uni['source'] = 'ai_only' 
        uni['reason'] = f"AI recommendation: {uni.get('reason', '')}"
        combined_recommendations.append(uni)
    
    # Sort by confidence (high first) then by score
    combined_recommendations.sort(key=lambda x: (
        0 if x.get('confidence') == 'high' else 1,
        -x.get('score', 0)
    ))
    
    verification_summary = {
        'ml_count': len(ml_results.get('recommendations', [])),
        'ai_count': len(gemini_results.get('recommendations', [])),
        'overlap_count': len(overlap_unis),
        'total_verified': len(combined_recommendations),
        'high_confidence_count': len([u for u in combined_recommendations if u.get('confidence') == 'high'])
    }
    
    return {
        'success': True,
        'source': 'ml_and_ai_verified',
        'needed_accommodations': combined_accommodations,
        'recommendations': combined_recommendations[:10],  # Top 10
        'verification_summary': verification_summary,
        'verification_note': f'Combined results from ML pipeline and Gemini AI. {verification_summary["high_confidence_count"]} high-confidence matches found.'
    }

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting UNIfy API server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    # Print available endpoints
    print("\n🚀 UNIfy API Server Starting...")
    print(f"📍 Server: http://{host}:{port}")
    print("📋 Available Endpoints:")
    print(f"   GET  /                    - Health check")
    print(f"   POST /api/recommendations - Main recommendations endpoint")
    print(f"   GET  /api/test           - Test with sample data")
    print(f"   POST /api/gemini         - Direct Gemini AI endpoint")
    print("\n🔗 Frontend Integration:")
    print(f"   Set your React app to call: http://{host}:{port}/api/recommendations")
    print("\n" + "="*50)
    
    app.run(host=host, port=port, debug=debug, threaded=True)


