"""
Flask API Application
Week 7 Project Module - Progressive Web Application

Main Flask application integrating all API endpoints
"""

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os

# Import API blueprints
from api.auth import auth_bp
from api.persons import persons_bp
from api.attendance import attendance_bp
from api.recognition import recognition_bp


def create_app(config=None):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', app.config['SECRET_KEY'])
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Apply custom config if provided
    if config:
        app.config.update(config)
    
    # Initialize extensions
    JWTManager(app)
    CORS(app, origins=os.environ.get('CORS_ORIGINS', '*').split(','))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(persons_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(recognition_bp)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'Face Recognition API is running',
            'version': '1.0.0'
        }), 200
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API info"""
        return jsonify({
            'name': 'Face Recognition Attendance API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'persons': '/api/persons',
                'attendance': '/api/attendance',
                'recognition': '/api/recognition',
                'health': '/api/health'
            },
            'documentation': '/api/docs'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


# Create app instance
app = create_app()


# Integration with previous weeks
"""
Week 1-5 Integration:
    The API endpoints in this application integrate all previous modules:
    
    /api/recognition/recognize:
        - Uses RecognitionService (Week 5)
        - Which uses FaceRecognizer (Week 3)
        - Which uses FaceDetector (Week 2)
        - Which uses image_utils (Week 1)
    
    /api/attendance/record:
        - Uses AttendanceService (Week 6)
        - Which uses RecognitionService (Week 5)
        - Saves to database (Week 6 models)

Complete flow example:
    1. Client uploads image → /api/recognition/recognize-and-record
    2. API processes with RecognitionService (weeks 1-5)
    3. API saves attendance with AttendanceService (week 6)
    4. Returns result to client
"""


if __name__ == "__main__":
    print("Flask API Application - Week 7 Project")
    print("=" * 50)
    print("\nRegistered endpoints:")
    print("  - POST   /api/auth/login")
    print("  - POST   /api/auth/register")
    print("  - POST   /api/auth/refresh")
    print("  - GET    /api/auth/me")
    print()
    print("  - GET    /api/persons/")
    print("  - POST   /api/persons/")
    print("  - GET    /api/persons/<id>")
    print("  - PUT    /api/persons/<id>")
    print("  - DELETE /api/persons/<id>")
    print("  - POST   /api/persons/<id>/upload-face")
    print()
    print("  - GET    /api/attendance/")
    print("  - GET    /api/attendance/today")
    print("  - POST   /api/attendance/record")
    print("  - GET    /api/attendance/status/<person_id>")
    print("  - GET    /api/attendance/report/daily")
    print("  - GET    /api/attendance/report/person/<id>")
    print()
    print("  - POST   /api/recognition/recognize")
    print("  - POST   /api/recognition/recognize-and-record")
    print("  - POST   /api/recognition/train")
    print("  - POST   /api/recognition/validate-face")
    print("  - GET    /api/recognition/statistics")
    print()
    print("  - GET    /api/health")
    print("  - GET    /")
    print("\n" + "=" * 50)
    print("\nStarting development server...")
    print("Access at: http://localhost:5000")
    print()
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
