"""
Attendance API Endpoints
Week 7 Project Module - Progressive Web Application

Attendance management endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, date

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

# Mock database (replace with actual database in production)
attendance_db = []
next_id = 1


@attendance_bp.route('/', methods=['GET'])
@jwt_required()
def get_attendances():
    """
    Get attendance records
    
    Query params:
        person_id: Filter by person
        date: Filter by date (YYYY-MM-DD)
        start_date: Start date for range
        end_date: End date for range
        type: Filter by type (check_in/check_out)
    
    Response:
        {
            "attendances": [...]
        }
    """
    try:
        person_id = request.args.get('person_id', type=int)
        target_date = request.args.get('date')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        attendance_type = request.args.get('type')
        
        # Filter records
        result = list(attendance_db)
        
        if person_id:
            result = [a for a in result if a['person_id'] == person_id]
        
        if target_date:
            target = datetime.fromisoformat(target_date).date()
            result = [a for a in result 
                     if datetime.fromisoformat(a['timestamp']).date() == target]
        
        if start_date and end_date:
            start = datetime.fromisoformat(start_date).date()
            end = datetime.fromisoformat(end_date).date()
            result = [a for a in result 
                     if start <= datetime.fromisoformat(a['timestamp']).date() <= end]
        
        if attendance_type:
            result = [a for a in result if a['type'] == attendance_type]
        
        return jsonify({'attendances': result}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@attendance_bp.route('/today', methods=['GET'])
@jwt_required()
def get_today_attendances():
    """
    Get today's attendance records
    
    Query params:
        person_id: Filter by person
    
    Response:
        {
            "date": "2024-01-15",
            "attendances": [...]
        }
    """
    try:
        person_id = request.args.get('person_id', type=int)
        today = date.today()
        
        # Filter today's records
        result = [a for a in attendance_db 
                 if datetime.fromisoformat(a['timestamp']).date() == today]
        
        if person_id:
            result = [a for a in result if a['person_id'] == person_id]
        
        return jsonify({
            'date': today.isoformat(),
            'attendances': result
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@attendance_bp.route('/record', methods=['POST'])
@jwt_required()
def record_attendance():
    """
    Record attendance manually
    
    Request body:
        {
            "person_id": 1,
            "type": "check_in",
            "confidence": 0.95,
            "location": "Main Office",
            "notes": "Manual entry"
        }
    
    Response:
        {
            "id": 1,
            "person_id": 1,
            "type": "check_in",
            ...
        }
    """
    try:
        global next_id
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        person_id = data.get('person_id')
        attendance_type = data.get('type')
        
        if not person_id or not attendance_type:
            return jsonify({'error': 'person_id and type are required'}), 400
        
        if attendance_type not in ['check_in', 'check_out']:
            return jsonify({'error': 'Invalid type. Must be check_in or check_out'}), 400
        
        # Create record
        record = {
            'id': next_id,
            'person_id': person_id,
            'timestamp': datetime.utcnow().isoformat(),
            'type': attendance_type,
            'confidence': data.get('confidence'),
            'photo_path': data.get('photo_path'),
            'location': data.get('location'),
            'notes': data.get('notes')
        }
        
        attendance_db.append(record)
        next_id += 1
        
        return jsonify(record), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@attendance_bp.route('/status/<int:person_id>', methods=['GET'])
@jwt_required()
def get_person_status(person_id):
    """
    Get current attendance status for person
    
    Response:
        {
            "person_id": 1,
            "status": "checked_in",
            "last_activity": "2024-01-15T08:30:00",
            "today_records": [...]
        }
    """
    try:
        today = date.today()
        
        # Get today's records for person
        today_records = [a for a in attendance_db 
                        if a['person_id'] == person_id 
                        and datetime.fromisoformat(a['timestamp']).date() == today]
        
        if not today_records:
            return jsonify({
                'person_id': person_id,
                'status': 'not_checked_in',
                'last_activity': None,
                'today_records': []
            }), 200
        
        # Get latest record
        latest = max(today_records, key=lambda x: x['timestamp'])
        
        status = 'checked_in' if latest['type'] == 'check_in' else 'checked_out'
        
        return jsonify({
            'person_id': person_id,
            'status': status,
            'last_activity': latest['timestamp'],
            'today_records': today_records
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@attendance_bp.route('/report/daily', methods=['GET'])
@jwt_required()
def get_daily_report():
    """
    Get daily attendance report
    
    Query params:
        date: Target date (YYYY-MM-DD), default: today
    
    Response:
        {
            "date": "2024-01-15",
            "total_persons": 10,
            "total_checked_in": 8,
            "total_checked_out": 5,
            "attendance_rate": 80.0,
            "records": [...]
        }
    """
    try:
        target_date = request.args.get('date')
        
        if target_date:
            target = datetime.fromisoformat(target_date).date()
        else:
            target = date.today()
        
        # Get records for date
        records = [a for a in attendance_db 
                  if datetime.fromisoformat(a['timestamp']).date() == target]
        
        # Calculate statistics
        person_ids = set(a['person_id'] for a in records)
        checked_in = len(set(a['person_id'] for a in records if a['type'] == 'check_in'))
        checked_out = len(set(a['person_id'] for a in records if a['type'] == 'check_out'))
        
        # Mock total persons (replace with actual count)
        total_persons = 10
        
        return jsonify({
            'date': target.isoformat(),
            'total_persons': total_persons,
            'total_checked_in': checked_in,
            'total_checked_out': checked_out,
            'attendance_rate': (checked_in / total_persons * 100) if total_persons > 0 else 0,
            'records': records
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@attendance_bp.route('/report/person/<int:person_id>', methods=['GET'])
@jwt_required()
def get_person_report(person_id):
    """
    Get attendance report for specific person
    
    Query params:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Response:
        {
            "person_id": 1,
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "total_days": 31,
            "days_attended": 20,
            "attendance_rate": 64.5,
            "records": [...]
        }
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date are required'}), 400
        
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()
        
        # Get records
        records = [a for a in attendance_db 
                  if a['person_id'] == person_id 
                  and start <= datetime.fromisoformat(a['timestamp']).date() <= end]
        
        # Calculate statistics
        days = (end - start).days + 1
        days_attended = len(set(datetime.fromisoformat(a['timestamp']).date() 
                               for a in records if a['type'] == 'check_in'))
        
        return jsonify({
            'person_id': person_id,
            'start_date': start.isoformat(),
            'end_date': end.isoformat(),
            'total_days': days,
            'days_attended': days_attended,
            'attendance_rate': (days_attended / days * 100) if days > 0 else 0,
            'records': records
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
