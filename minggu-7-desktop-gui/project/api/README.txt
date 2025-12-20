API Endpoints (Optional)
========================

Week 7 includes optional REST API for attendance system.

To use API:
1. Install: pip install flask flask-cors
2. Check if api files exist in this folder
3. Run: python api/server.py
4. Access: http://localhost:5000

API endpoints:
  GET  /api/attendance - List all attendance
  POST /api/check-in   - Record check-in
  POST /api/check-out  - Record check-out
  GET  /api/reports    - Generate reports
