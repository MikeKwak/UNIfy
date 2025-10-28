"""
UNIfy Flask API Server
Provides REST API endpoints for the React frontend to access ML/AI recommendations.
"""

from gemini_recommender import get_gemini_recommendations
from ml_pipeline import get_recommendations
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def validate_student_profile(data: dict):
    required_fields = ['mental_health',
                       'physical_health', 'courses', 'gpa', 'severity']
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    try:
        gpa = float(data['gpa'])
    except (TypeError, ValueError):
        return False, "GPA must be a valid number"
    if not 0.0 <= gpa <= 4.0:
        return False, "GPA must be between 0.0 and 4.0"
    if data['severity'] not in ['mild', 'moderate', 'severe']:
        return False, "Severity must be one of: mild, moderate, severe"
    return True, ""


# Import our ML/AI systems

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def error_response(message: str, status: int = 400, code: str = "BAD_REQUEST"):
    return jsonify({"success": False, "error": {"code": code, "message": message}}), status


# Initialize Flask app
app = Flask(__name__)
# For production, restrict CORS to your real frontend domain
PROD_FRONTEND_ORIGIN = os.environ.get("PROD_FRONTEND_ORIGIN", "https://your-production-frontend.com")
if os.environ.get("FLASK_ENV") == "production":
    CORS(app, resources={r"/*": {"origins": PROD_FRONTEND_ORIGIN}}, supports_credentials=True)
else:
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

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
            return error_response("Request must be JSON", 400, "NOT_JSON")

        data = request.get_json()
        ok, msg = validate_student_profile(data)
        if not ok:
            return error_response(msg, 400, "VALIDATION_ERROR")

        student_profile = {
            'mental_health': str(data['mental_health']),
            'physical_health': str(data['physical_health']),
            'courses': str(data['courses']),
            'gpa': float(data['gpa']),
            'severity': str(data['severity'])
        }

        logger.info(
            f"Processing recommendation request for: {student_profile}")

        # Get recommendations from ML/AI pipeline
        result = get_recommendations(student_profile)

        logger.info(
            f"Recommendation result: success={result['success']}, source={result.get('source', 'unknown')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in recommendations endpoint: {str(e)}")
        return error_response("Internal server error", 500, "INTERNAL_ERROR")


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
        return error_response("Internal server error", 500, "INTERNAL_ERROR")


@app.route('/api/gemini', methods=['POST'])
def get_gemini_recommendations_endpoint():
    """
    Direct Gemini AI endpoint for testing.

    Expected JSON payload: same as /api/recommendations
    """
    try:
        if not request.is_json:
            return error_response("Request must be JSON", 400, "NOT_JSON")

        data = request.get_json()

        # Create student profile (same validation as main endpoint)
        required_fields = ['mental_health',
                           'physical_health', 'courses', 'gpa', 'severity']
        missing_fields = [
            field for field in required_fields if field not in data]

        if missing_fields:
            return error_response(f'Missing required fields: {", ".join(missing_fields)}', 400, "VALIDATION_ERROR")

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

        logger.info(
            f"Gemini AI result: success={result['success']}, source={result.get('source', 'unknown')}")

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in Gemini endpoint: {str(e)}")
        return error_response("Internal server error", 500, "INTERNAL_ERROR")


@app.route('/api/roadmap', methods=['POST'])
def generate_roadmap_svg():
    """
    Generate a dynamic roadmap SVG based on user/session data.
    Expects JSON payload with relevant roadmap info.
    Returns SVG as image/svg+xml.
    """
    try:
        if not request.is_json:
            return error_response("Request must be JSON", 400, "NOT_JSON")
        data = request.get_json()
        # Example: use university name and steps from payload
        university = data.get('university', 'Your University')
        steps = data.get('steps', [
            'Eligibility & Prerequisites',
            'Required Documents',
            'Application Submission',
            'Decision & Next Steps'
        ])
        # Simple SVG generation (customize as needed)
        svg = f'''<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#F7FEE7" />
            <text x="50%" y="40" text-anchor="middle" font-size="28" fill="#92BD3A">Roadmap for {university}</text>
            '''
        for i, step in enumerate(steps):
            y = 80 + i * 30
            svg += f'<circle cx="60" cy="{y}" r="12" fill="#92BD3A" />'
            svg += f'<text x="90" y="{y+5}" font-size="18" fill="#333">{step}</text>'
        svg += '</svg>'
        return Response(svg, mimetype='image/svg+xml')
    except Exception as e:
        logger.error(f"Error in roadmap endpoint: {str(e)}")
        return error_response("Internal server error", 500, "INTERNAL_ERROR")


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return error_response("Endpoint not found", 404, "NOT_FOUND")


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return error_response("Internal server error", 500, "INTERNAL_ERROR")


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
    print(
        f"   Set your React app to call: http://{host}:{port}/api/recommendations")
    print("\n" + "="*50)

    app.run(host=host, port=port, debug=debug, threaded=True)
