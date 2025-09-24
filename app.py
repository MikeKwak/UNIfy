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
from gemini_recommender import get_gemini_recommendations

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
