"""
Authentication API Endpoints
Week 7 Project Module - Progressive Web Application

JWT authentication for Flask REST API
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# In-memory user store (replace with database in production)
users = {
    'admin': {
        'username': 'admin',
        'password': generate_password_hash('admin123'),
        'role': 'admin'
    }
}


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login endpoint
    
    Request body:
        {
            "username": "admin",
            "password": "admin123"
        }
    
    Response:
        {
            "access_token": "...",
            "refresh_token": "...",
            "user": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Check user exists
        user = users.get(username)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create tokens
        access_token = create_access_token(
            identity=username,
            additional_claims={'role': user['role']},
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=username,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'username': user['username'],
                'role': user['role']
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    
    Headers:
        Authorization: Bearer <refresh_token>
    
    Response:
        {
            "access_token": "..."
        }
    """
    try:
        current_user = get_jwt_identity()
        user = users.get(current_user)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create new access token
        access_token = create_access_token(
            identity=current_user,
            additional_claims={'role': user['role']},
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify({'access_token': access_token}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user info
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "username": "admin",
            "role": "admin"
        }
    """
    try:
        current_user = get_jwt_identity()
        user = users.get(current_user)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'username': user['username'],
            'role': user['role']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register new user (admin only in production)
    
    Request body:
        {
            "username": "newuser",
            "password": "password123",
            "role": "user"
        }
    
    Response:
        {
            "message": "User registered successfully",
            "user": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Check if user exists
        if username in users:
            return jsonify({'error': 'Username already exists'}), 409
        
        # Create user
        users[username] = {
            'username': username,
            'password': generate_password_hash(password),
            'role': role
        }
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'username': username,
                'role': role
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
