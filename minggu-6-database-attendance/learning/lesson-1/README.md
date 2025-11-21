# Lesson 1: MySQL Setup & Attendance Logic

## Tujuan
- Setup MySQL database
- Create tables (Person, Attendance)
- Implement attendance logic
- Prevent duplicate check-ins

## Database Schema
```sql
Person: id, name, created_date
Attendance: id, person_id, check_in_time, date
```

## Attendance Rules
1. One check-in per person per day
2. Auto-generate timestamp
3. Validate person exists

## Langkah
1. Install MySQL
2. Create database: `attendance_db`
3. Run: `python main.py`
4. Tables will be created
5. Test attendance recording

## Next: Lesson 2 - Reports & Analytics
