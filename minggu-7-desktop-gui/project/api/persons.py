"""
Persons API Endpoints
Week 7 Project Module - Progressive Web Application

CRUD operations for persons (employees)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
from werkzeug.utils import secure_filename

persons_bp = Blueprint('persons', __name__, url_prefix='/api/persons')

# Mock database (replace with actual database in production)
persons_db = {}
next_id = 1


@persons_bp.route('/', methods=['GET'])
@jwt_required()
def get_persons():
    """
    Get all persons
    
    Query params:
        department: Filter by department
        is_active: Filter by active status (true/false)
    
    Response:
        {
            "persons": [...]
        }
    """
    try:
        department = request.args.get('department')
        is_active = request.args.get('is_active')
        
        # Filter persons
        result = list(persons_db.values())
        
        if department:
            result = [p for p in result if p.get('department') == department]
        
        if is_active is not None:
            active = is_active.lower() == 'true'
            result = [p for p in result if p.get('is_active') == active]
        
        return jsonify({'persons': result}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@persons_bp.route('/<int:person_id>', methods=['GET'])
@jwt_required()
def get_person(person_id):
    """
    Get person by ID
    
    Response:
        {
            "id": 1,
            "name": "John Doe",
            ...
        }
    """
    try:
        person = persons_db.get(person_id)
        
        if not person:
            return jsonify({'error': 'Person not found'}), 404
        
        return jsonify(person), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@persons_bp.route('/', methods=['POST'])
@jwt_required()
def create_person():
    """
    Create new person
    
    Request body:
        {
            "name": "John Doe",
            "employee_id": "EMP001",
            "department": "IT",
            "email": "john@example.com",
            "phone": "+1234567890"
        }
    
    Response:
        {
            "id": 1,
            "name": "John Doe",
            ...
        }
    """
    try:
        global next_id
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Name is required'}), 400
        
        # Check employee_id uniqueness
        employee_id = data.get('employee_id')
        if employee_id:
            existing = [p for p in persons_db.values() if p.get('employee_id') == employee_id]
            if existing:
                return jsonify({'error': 'Employee ID already exists'}), 409
        
        # Create person
        person = {
            'id': next_id,
            'name': name,
            'employee_id': employee_id,
            'department': data.get('department'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'is_active': True
        }
        
        persons_db[next_id] = person
        next_id += 1
        
        return jsonify(person), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@persons_bp.route('/<int:person_id>', methods=['PUT'])
@jwt_required()
def update_person(person_id):
    """
    Update person
    
    Request body:
        {
            "name": "John Doe Updated",
            "department": "HR",
            ...
        }
    
    Response:
        {
            "id": 1,
            "name": "John Doe Updated",
            ...
        }
    """
    try:
        person = persons_db.get(person_id)
        
        if not person:
            return jsonify({'error': 'Person not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update fields
        if 'name' in data:
            person['name'] = data['name']
        if 'employee_id' in data:
            # Check uniqueness
            existing = [p for p in persons_db.values() 
                       if p.get('employee_id') == data['employee_id'] and p['id'] != person_id]
            if existing:
                return jsonify({'error': 'Employee ID already exists'}), 409
            person['employee_id'] = data['employee_id']
        if 'department' in data:
            person['department'] = data['department']
        if 'email' in data:
            person['email'] = data['email']
        if 'phone' in data:
            person['phone'] = data['phone']
        if 'is_active' in data:
            person['is_active'] = data['is_active']
        
        return jsonify(person), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@persons_bp.route('/<int:person_id>', methods=['DELETE'])
@jwt_required()
def delete_person(person_id):
    """
    Delete person (soft delete - set is_active to False)
    
    Response:
        {
            "message": "Person deleted successfully"
        }
    """
    try:
        person = persons_db.get(person_id)
        
        if not person:
            return jsonify({'error': 'Person not found'}), 404
        
        # Soft delete
        person['is_active'] = False
        
        return jsonify({'message': 'Person deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@persons_bp.route('/<int:person_id>/upload-face', methods=['POST'])
@jwt_required()
def upload_face(person_id):
    """
    Upload face image for person
    
    Request: multipart/form-data
        file: Image file
        angle: frontal/left/right (optional)
    
    Response:
        {
            "message": "Face uploaded successfully",
            "file_path": "..."
        }
    """
    try:
        person = persons_db.get(person_id)
        
        if not person:
            return jsonify({'error': 'Person not found'}), 404
        
        # Check file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if ext not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg'}), 400
        
        # Get angle
        angle = request.form.get('angle', 'frontal')
        
        # Save file
        filename = secure_filename(f"{person_id}_{angle}.{ext}")
        upload_folder = 'uploads/faces'
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        return jsonify({
            'message': 'Face uploaded successfully',
            'file_path': file_path
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
