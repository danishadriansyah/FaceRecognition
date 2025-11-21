# Minggu 7 - Learning: Desktop GUI & RESTful API

## 📚 Overview
Folder ini berisi 2 tutorial files untuk build desktop GUI application menggunakan Tkinter dan RESTful API dengan Flask untuk remote access.

## 📁 File Structure

```
learning/
├── README.md (file ini)
├── 02_restful_api_design.py
└── 03_authentication.py
```

---

## 🎯 Tutorial Files - Detailed Guide

### 02_restful_api_design.py
**Tujuan:** Build RESTful API untuk attendance system dengan Flask

**Apa yang dipelajari:**
- Flask basics dan routing
- RESTful API design principles
- JSON request/response handling
- API endpoints untuk CRUD operations
- Error handling dan status codes
- API documentation
- Cross-Origin Resource Sharing (CORS)

**Cara menggunakan:**
```bash
cd minggu-7-desktop-gui/learning
pip install flask flask-cors
python 02_restful_api_design.py
```

**Output yang diharapkan:**
```
* Running on http://127.0.0.1:5000/
* Press CTRL+C to quit

API Endpoints:
  GET    /api/employees
  POST   /api/employees
  GET    /api/employees/<id>
  PUT    /api/employees/<id>
  DELETE /api/employees/<id>
  GET    /api/attendance/today
  POST   /api/attendance/checkin
  POST   /api/attendance/checkout
  GET    /api/reports/daily
  GET    /api/reports/monthly
```

**Flask API implementation:**

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from attendance_system import AttendanceSystem
from datetime import datetime, date
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for web clients

# Initialize attendance system
attendance = AttendanceSystem(
    db_path='attendance.db',
    dataset_path='dataset/'
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function for standardized responses
def api_response(data=None, message=None, status=200, error=None):
    response = {
        'success': error is None,
        'timestamp': datetime.now().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    if error:
        response['error'] = error
    
    return jsonify(response), status

# ==================== EMPLOYEE ENDPOINTS ====================

@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Get all employees"""
    try:
        employees = attendance.get_all_employees()
        return api_response(data=employees)
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        return api_response(error=str(e), status=500)

@app.route('/api/employees', methods=['POST'])
def add_employee():
    """Add new employee"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['employee_id', 'name', 'department']
        if not all(field in data for field in required):
            return api_response(
                error=f"Missing required fields: {required}",
                status=400
            )
        
        # Add employee
        success = attendance.add_employee(
            employee_id=data['employee_id'],
            name=data['name'],
            department=data['department'],
            email=data.get('email'),
            phone=data.get('phone')
        )
        
        if success:
            return api_response(
                message=f"Employee {data['name']} added successfully",
                status=201
            )
        else:
            return api_response(
                error="Failed to add employee",
                status=400
            )
    
    except Exception as e:
        logger.error(f"Error adding employee: {e}")
        return api_response(error=str(e), status=500)

@app.route('/api/employees/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get single employee details"""
    try:
        employee = attendance.get_employee_info(employee_id)
        
        if employee:
            return api_response(data=employee)
        else:
            return api_response(
                error=f"Employee {employee_id} not found",
                status=404
            )
    
    except Exception as e:
        logger.error(f"Error fetching employee: {e}")
        return api_response(error=str(e), status=500)

@app.route('/api/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update employee information"""
    try:
        data = request.get_json()
        
        success = attendance.update_employee(
            employee_id=employee_id,
            **data
        )
        
        if success:
            return api_response(
                message=f"Employee {employee_id} updated"
            )
        else:
            return api_response(
                error="Failed to update employee",
                status=400
            )
    
    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        return api_response(error=str(e), status=500)

@app.route('/api/employees/<employee_id>', methods=['DELETE'])
def deactivate_employee(employee_id):
    """Deactivate employee"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'Not specified')
        
        success = attendance.deactivate_employee(
            employee_id=employee_id,
            reason=reason
        )
        
        if success:
            return api_response(
                message=f"Employee {employee_id} deactivated"
            )
        else:
            return api_response(
                error="Failed to deactivate employee",
                status=400
            )
    
    except Exception as e:
        logger.error(f"Error deactivating employee: {e}")
        return api_response(error=str(e), status=500)

# ==================== ATTENDANCE ENDPOINTS ====================

@app.route('/api/attendance/today', methods=['GET'])
def get_today_attendance():
    """Get today's attendance"""
    try:
        report = attendance.get_daily_report()
        return api_response(data=report)
    
    except Exception as e:
        logger.error(f"Error fetching attendance: {e}")
        return api_response(error=str(e), status=500)

@app.route('/api/attendance/checkin', methods=['POST'])
def check_in():
    """Mark check-in for employee"""
    try:
        data = request.get_json()
        
        if 'employee_id' not in data:
            return api_response(
                error="employee_id required",
                status=400
            )
        
        result = attendance.mark_attendance_manual(
            employee_id=data['employee_id'],
            action='check_in',
            notes=data.get('notes')
        )
        
        if result['success']:
            return api_response(
                data=result,
                message=f"Check-in recorded: {result['status']}"
            )
        else:
            return api_response(
                error=result.get('message', 'Check-in failed'),
                status=400
            )
    
    except Exception as e:
        logger.error(f"Error during check-in: {e}")
        return api_response(error=str(e), status=500)

@app.route('/api/attendance/checkout', methods=['POST'])
def check_out():
    """Mark check-out for employee"""
    try:
        data = request.get_json()
        
        if 'employee_id' not in data:
            return api_response(
                error="employee_id required",
                status=400
            )
        
        result = attendance.mark_attendance_manual(
            employee_id=data['employee_id'],
            action='check_out'
        )
        
        if result['success']:
            return api_response(
                data=result,
                message=f"Check-out recorded. Hours: {result['working_hours']:.2f}"
            )
        else:
            return api_response(
                error=result.get('message', 'Check-out failed'),
                status=400
            )
    
    except Exception as e:
        logger.error(f"Error during check-out: {e}")
        return api_response(error=str(e), status=500)

# ==================== REPORTS ENDPOINTS ====================

@app.route('/api/reports/daily', methods=['GET'])
def daily_report():
    """Get daily attendance report"""
    try:
        date_str = request.args.get('date')
        
        if date_str:
            report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            report_date = date.today()
        
        report = attendance.get_daily_report(date=report_date)
        return api_response(data=report)
    
    except ValueError:
        return api_response(
            error="Invalid date format. Use YYYY-MM-DD",
            status=400
        )
    except Exception as e:
        logger.error(f"Error generating daily report: {e}")
        return api_response(error=str(e), status=500)

@app.route('/api/reports/monthly', methods=['GET'])
def monthly_report():
    """Get monthly attendance report"""
    try:
        year = int(request.args.get('year', date.today().year))
        month = int(request.args.get('month', date.today().month))
        
        report = attendance.generate_monthly_report(
            year=year,
            month=month
        )
        
        return api_response(data=report)
    
    except ValueError:
        return api_response(
            error="Invalid year or month",
            status=400
        )
    except Exception as e:
        logger.error(f"Error generating monthly report: {e}")
        return api_response(error=str(e), status=500)

@app.route('/api/reports/employee/<employee_id>', methods=['GET'])
def employee_report(employee_id):
    """Get employee attendance history"""
    try:
        year = int(request.args.get('year', date.today().year))
        month = int(request.args.get('month', date.today().month))
        
        history = attendance.get_employee_history(
            employee_id=employee_id,
            year=year,
            month=month
        )
        
        return api_response(data=history)
    
    except Exception as e:
        logger.error(f"Error fetching employee history: {e}")
        return api_response(error=str(e), status=500)

# ==================== STATISTICS ENDPOINTS ====================

@app.route('/api/stats/department', methods=['GET'])
def department_stats():
    """Get department-wise statistics"""
    try:
        date_str = request.args.get('date')
        
        if date_str:
            stats_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            stats_date = date.today()
        
        stats = attendance.get_department_summary(date=stats_date)
        return api_response(data=stats)
    
    except Exception as e:
        logger.error(f"Error fetching department stats: {e}")
        return api_response(error=str(e), status=500)

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return api_response(
        data={
            'status': 'healthy',
            'version': '1.0.0',
            'database': 'connected'
        },
        message='API is running'
    )

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'name': 'Attendance System API',
        'version': '1.0.0',
        'endpoints': {
            'employees': {
                'GET /api/employees': 'List all employees',
                'POST /api/employees': 'Add new employee',
                'GET /api/employees/<id>': 'Get employee details',
                'PUT /api/employees/<id>': 'Update employee',
                'DELETE /api/employees/<id>': 'Deactivate employee'
            },
            'attendance': {
                'GET /api/attendance/today': "Today's attendance",
                'POST /api/attendance/checkin': 'Mark check-in',
                'POST /api/attendance/checkout': 'Mark check-out'
            },
            'reports': {
                'GET /api/reports/daily': 'Daily report',
                'GET /api/reports/monthly': 'Monthly report',
                'GET /api/reports/employee/<id>': 'Employee history'
            },
            'stats': {
                'GET /api/stats/department': 'Department statistics'
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Testing the API:**

```bash
# Test with curl

# Get all employees
curl http://localhost:5000/api/employees

# Add employee
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{"employee_id":"001","name":"Alice","department":"IT"}'

# Check-in
curl -X POST http://localhost:5000/api/attendance/checkin \
  -H "Content-Type: application/json" \
  -d '{"employee_id":"001"}'

# Get daily report
curl http://localhost:5000/api/reports/daily?date=2025-11-14

# Get department stats
curl http://localhost:5000/api/stats/department
```

**Testing with Python requests:**

```python
import requests
import json

BASE_URL = 'http://localhost:5000/api'

# Add employee
response = requests.post(
    f'{BASE_URL}/employees',
    json={
        'employee_id': '001',
        'name': 'Alice Johnson',
        'department': 'Engineering',
        'email': 'alice@company.com'
    }
)
print(response.json())

# Mark check-in
response = requests.post(
    f'{BASE_URL}/attendance/checkin',
    json={'employee_id': '001'}
)
print(response.json())

# Get today's report
response = requests.get(f'{BASE_URL}/reports/daily')
report = response.json()
print(f"Present: {report['data']['present']}")
```

---

### 03_authentication.py
**Tujuan:** Add authentication dan authorization ke API

**Apa yang dipelajari:**
- JWT (JSON Web Tokens) authentication
- User roles dan permissions
- Protected endpoints
- Session management
- Password hashing
- Token refresh mechanism

**Cara menggunakan:**
```bash
pip install flask-jwt-extended
python 03_authentication.py
```

**Output yang diharapkan:**
- Secure API with login
- Token-based authentication
- Role-based access control
- Protected endpoints

**Authentication implementation:**

```python
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import sqlite3

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

# ==================== USER MANAGEMENT ====================

def init_users_db():
    """Initialize users database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            email VARCHAR(100),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create default admin if not exists
    admin_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password_hash, role, email)
        VALUES ('admin', ?, 'admin', 'admin@company.com')
    ''', (admin_hash,))
    
    conn.commit()
    conn.close()

init_users_db()

def get_user_by_username(username):
    """Fetch user from database"""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT * FROM users WHERE username = ? AND is_active = 1',
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Username and password required'
            }), 400
        
        # Fetch user
        user = get_user_by_username(username)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        # Verify password
        if not check_password_hash(user['password_hash'], password):
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        # Create tokens
        access_token = create_access_token(
            identity=username,
            additional_claims={'role': user['role']}
        )
        refresh_token = create_refresh_token(identity=username)
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'username': user['username'],
                    'role': user['role'],
                    'email': user['email']
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    current_user = get_jwt_identity()
    user = get_user_by_username(current_user)
    
    new_token = create_access_token(
        identity=current_user,
        additional_claims={'role': user['role']}
    )
    
    return jsonify({
        'success': True,
        'data': {'access_token': new_token}
    }), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'user')
        
        # Validate
        if not username or not password:
            return jsonify({
                'success': False,
                'error': 'Username and password required'
            }), 400
        
        # Check if exists
        if get_user_by_username(username):
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 400
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Insert user
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, email)
            VALUES (?, ?, ?, ?)
        ''', (username, password_hash, role, email))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'User {username} registered successfully'
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== PROTECTED ENDPOINTS ====================

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    """Protected endpoint - requires valid token"""
    current_user = get_jwt_identity()
    claims = get_jwt()
    
    return jsonify({
        'success': True,
        'message': f'Hello {current_user}!',
        'data': {
            'username': current_user,
            'role': claims.get('role')
        }
    }), 200

def admin_required():
    """Decorator for admin-only endpoints"""
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify({
                    'success': False,
                    'error': 'Admin access required'
                }), 403
            return fn(*args, **kwargs)
        decorator.__name__ = fn.__name__
        return decorator
    return wrapper

@app.route('/api/admin/users', methods=['GET'])
@admin_required()
def get_all_users():
    """Admin only - Get all users"""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id, username, role, email, created_at FROM users')
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'data': users
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Using authenticated API:**

```python
import requests

BASE_URL = 'http://localhost:5000/api'

# 1. Login
response = requests.post(
    f'{BASE_URL}/auth/login',
    json={
        'username': 'admin',
        'password': 'admin123'
    }
)

tokens = response.json()['data']
access_token = tokens['access_token']

# 2. Use protected endpoint
headers = {'Authorization': f'Bearer {access_token}'}

response = requests.get(
    f'{BASE_URL}/protected',
    headers=headers
)
print(response.json())

# 3. Admin endpoint
response = requests.get(
    f'{BASE_URL}/admin/users',
    headers=headers
)
print(response.json())
```

---

## 🎓 Best Practices

### API Design
- **RESTful conventions:** Use proper HTTP methods
- **Versioning:** Include version in URL (/api/v1/)
- **Pagination:** Limit large result sets
- **Filtering:** Support query parameters
- **Documentation:** Auto-generate API docs

### Security
- **HTTPS:** Use SSL in production
- **Authentication:** JWT or OAuth2
- **Rate limiting:** Prevent abuse
- **Input validation:** Sanitize all inputs
- **CORS:** Configure properly

### Error Handling
- **Status codes:** Use appropriate HTTP codes
- **Error messages:** Clear and helpful
- **Logging:** Log all errors
- **Consistency:** Uniform error format

---

## ✅ Checklist Progress

```
[ ] 02_restful_api_design.py - API running, endpoints tested
[ ] 03_authentication.py - Login working, tokens validated
[ ] API documentation created
[ ] Postman collection exported
[ ] Security measures implemented
```

---

## 🐛 Common Issues & Solutions

**CORS errors:**
- Install flask-cors
- Configure allowed origins
- Include credentials if needed

**Token expiration:**
- Implement refresh token logic
- Store tokens securely
- Handle 401 responses

**Database connection:**
- Use connection pooling
- Close connections properly
- Handle timeout errors

---

## ⏭️ Next Steps

Setelah minggu 7:

1. ✅ RESTful API operational
2. ✅ Authentication working
3. ✅ All endpoints tested
4. ✅ Lanjut ke **Minggu 8: Final Testing & Deployment**

---

**APIs connect everything! 🔌**

*Good API = Happy developers!*
