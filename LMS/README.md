# LMS (Learning Management System) - Complete Project Guide

## Project Overview

A comprehensive Learning Management System built with Django, Django REST Framework, and JWT authentication. This system supports role-based access control (Admin, Instructor, Student) with course management, lesson planning, assignment tracking, and grading capabilities.

---

## Table of Contents

1. [Features](#features)
2. [Core Models](#core-models)
3. [Installation & Setup](#installation--setup)
4. [Running the Project](#running-the-project)
5. [API Endpoints](#api-endpoints)
6. [Frontend Pages](#frontend-pages)
7. [User Roles & Permissions](#user-roles--permissions)
8. [Database Structure](#database-structure)
9. [Future Improvements](#future-improvements)
10. [Troubleshooting](#troubleshooting)

---

## Features

### ✅ Core Features Implemented

- ✅ **User Registration & Login** - JWT Authentication with token refresh
- ✅ **Role-Based Users** - Admin, Instructor, Student roles
- ✅ **Course Creation & Management** - Instructors can create and manage courses
- ✅ **Lesson Management** - Create and organize lessons within courses
- ✅ **Assignment Creation** - Create assignments with due dates and points
- ✅ **Student Assignment Submission** - Students can submit assignments
- ✅ **Grading System** - Instructors can grade submissions with feedback
- ✅ **JWT Authentication** - Secure API authentication with access/refresh tokens
- ✅ **API Documentation** - Auto-generated API docs at `/api/docs/`
- ✅ **DRF Integration** - RESTful API with Django REST Framework
- ✅ **CORS Support** - Cross-Origin Resource Sharing configured
- ✅ **Admin Interface** - Custom Django admin with all models registered

---

## Core Models

### 1. **CustomUser** (users app)
```python
- username (CharField)
- email (EmailField)
- password (PasswordField)
- role (CharField) - Choices: admin, instructor, student
- is_teacher (BooleanField) - Legacy field for backward compatibility
- is_staff (BooleanField)
- is_superuser (BooleanField)
- date_joined (DateTimeField)
```

### 2. **Course** (courses app)
```python
- id (AutoField)
- title (CharField, max_length=200)
- description (TextField)
- teacher (ForeignKey to CustomUser)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```

### 3. **Lesson**
```python
- id (AutoField)
- course (ForeignKey to Course)
- title (CharField, max_length=200)
- description (TextField)
- content (TextField)
- order (IntegerField)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```

### 4. **Assignment**
```python
- id (AutoField)
- course (ForeignKey to Course)
- title (CharField, max_length=200)
- description (TextField)
- due_date (DateTimeField)
- points (IntegerField, 1-1000)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```

### 5. **Submission**
```python
- id (AutoField)
- assignment (ForeignKey to Assignment)
- student (ForeignKey to CustomUser)
- content (TextField)
- submission_text (TextField)
- status (CharField) - Choices: draft, submitted, graded, returned
- submitted_at (DateTimeField, nullable)
- grade (IntegerField, 0-100, nullable)
- feedback (TextField, blank)
- graded_at (DateTimeField, nullable)
- graded_by (ForeignKey to CustomUser, nullable)
- created_at (DateTimeField, auto_now_add=True)
- updated_at (DateTimeField, auto_now=True)
```

### 6. **Enrollment**
```python
- id (AutoField)
- student (ForeignKey to CustomUser)
- course (ForeignKey to Course)
- completed (BooleanField, default=False)
- completed_at (DateTimeField, nullable)
- enrolled_at (DateTimeField, auto_now_add=True)
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual Environment (recommended)

### Step 1: Clone/Setup Project
```bash
cd "c:\Users\Lakshay Bishnoi\OneDrive\Desktop\study\pep project\final_lms_project"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# Activate virtual environment
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install Django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install coreapi
pip install python-decouple
```

### Step 4: Configure Database
```bash
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
# Enter username, email, and password
```

### Step 6: Populate Test Data (Optional)
```bash
python manage.py populate_test_data
```

This creates:
- **Admin**: Username: `admin`, Password: `password`
- **Instructor**: Username: `teacher`, Password: `password`
- **Student**: Username: `student`, Password: `password`

---

## Running the Project

### Start Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

Server will be available at: `http://localhost:8000`

### Access Points

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/` | Home page |
| `http://localhost:8000/courses/` | Course listing |
| `http://localhost:8000/users/login/` | Login page |
| `http://localhost:8000/users/register/` | Registration page |
| `http://localhost:8000/admin/` | Django admin panel |
| `http://localhost:8000/api/` | API root |
| `http://localhost:8000/api/docs/` | API documentation |

---

## API Endpoints

### Authentication

#### 1. Register New User
```
POST /users/api/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "role": "student",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### 2. Login (Obtain JWT Tokens)
```
POST /users/api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3. Refresh Token
```
POST /users/api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Courses

#### 1. List All Courses
```
GET /api/courses/
Authorization: Bearer {access_token}
```

#### 2. Create Course (Instructor Only)
```
POST /api/courses/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Advanced Python Programming",
  "description": "Learn advanced Python concepts"
}
```

#### 3. Get Course Detail
```
GET /api/courses/{id}/
Authorization: Bearer {access_token}
```

#### 4. Enroll in Course
```
POST /api/courses/{id}/enroll/
Authorization: Bearer {access_token}
```

#### 5. Check Enrollment Status
```
GET /api/courses/{id}/check_enrollment/
Authorization: Bearer {access_token}
```

### Lessons

#### 1. List Lessons (by course)
```
GET /api/lessons/?course_id={course_id}
Authorization: Bearer {access_token}
```

#### 2. Create Lesson (Instructor Only)
```
POST /api/lessons/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "course": {course_id},
  "title": "Introduction to Functions",
  "description": "Learn about Python functions",
  "content": "Functions are reusable blocks of code...",
  "order": 1
}
```

### Assignments

#### 1. List Assignments (by course)
```
GET /api/assignments/?course_id={course_id}
Authorization: Bearer {access_token}
```

#### 2. Create Assignment (Instructor Only)
```
POST /api/assignments/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "course": {course_id},
  "title": "Assignment 1: Write a Function",
  "description": "Write a function that adds two numbers",
  "due_date": "2026-03-01T23:59:59Z",
  "points": 50
}
```

#### 3. Get Assignment Submissions (Instructor Only)
```
GET /api/assignments/{id}/submissions/
Authorization: Bearer {access_token}
```

### Submissions

#### 1. Create Submission (Student Only)
```
POST /api/submissions/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "assignment": {assignment_id},
  "submission_text": "# My Solution\n\ndef add(a, b):\n    return a + b\n\nprint(add(5, 3))"
}
```

#### 2. Get My Submissions (Student)
```
GET /api/submissions/my_submissions/
Authorization: Bearer {access_token}
```

#### 3. Grade Submission (Instructor Only)
```
POST /api/submissions/{id}/grade/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "grade": 85,
  "feedback": "Great work! Your solution is correct and well-structured.",
  "status": "graded"
}
```

### Enrollments

#### 1. Get User's Enrolled Courses
```
GET /api/enrollments/my_courses/
Authorization: Bearer {access_token}
```

#### 2. List All Enrollments (Paginated)
```
GET /api/enrollments/
Authorization: Bearer {access_token}
```

### User Management

#### 1. Get Current User Profile
```
GET /users/api/me/
Authorization: Bearer {access_token}
```

#### 2. Change Password
```
POST /users/api/change_password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "old_password": "currentpassword",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

---

## Frontend Pages

### 1. **index.html** - Home/Dashboard
- Welcome message based on authentication status
- Role-based action buttons
- Feature highlights
- Test credentials information

### 2. **login.html** - Login Page
- Email/Username input
- Password input
- Modern gradient design
- Forgot password link

### 3. **register.html** - Registration Page
- User registration form
- Role selection (Admin, Instructor, Student)
- Email validation

### 4. **home.html** - Home Dashboard
- Authenticated user greeting
- Role-based menu options
- Direct access to courses
- Teacher options for creating courses

### 5. **course_list.html** - Browse All Courses
- Display all available courses
- Search and filter capabilities
- Enrollment buttons for students
- Delete button for instructors (own courses)

### 6. **my_courses.html** - Student's Enrolled Courses
- List of enrolled courses
- Course progress
- Mark as complete button
- Access to assignments

### 7. **create_course.html** - Create New Course
- Course title input
- Course description textarea
- Submit button (Teachers only)

### 8. **assignments.html** - View Course Assignments
- List of assignments for a course
- Due dates and point values
- Submit/View submissions buttons

### 9. **assignment_submit.html** - Submit Assignment
- Assignment details
- Text submission area
- Status display for existing submissions
- Update/Submit buttons

### 10. **view_submissions.html** - Grade Submissions (Instructor)
- Table of all submissions
- Student names and submission status
- Grade and feedback display
- Grade/Update button for each submission

### 11. **grade_submission.html** - Grade an Assignment
- Student submission display
- Grade input (0-100)
- Feedback textarea
- Submit grades button

### 12. **submission_detail.html** - View Submission Details
- Complete submission information
- Grade and feedback from instructor
- Submission content in formatted view

---

## User Roles & Permissions

### Admin Role
- Access to all admin functions
- User management
- System-wide settings
- View all content
- Can perform any action

### Instructor Role
- Create and manage courses
- Create lessons and assignments
- Set due dates and points
- Grade student submissions
- View student progress
- Cannot enroll in courses as student

### Student Role
- Enroll in courses
- View course materials and lessons
- Submit assignments
- View grades and feedback
- Cannot create courses
- Cannot access grading functions

---

## Database Structure

### ER Diagram (Text Representation)

```
CustomUser
├── id (PK)
├── username
├── email
├── password
├── role (admin, instructor, student)
└── is_teacher (legacy field)

Course
├── id (PK)
├── title
├── description
├── teacher_id (FK to CustomUser)
├── created_at
└── updated_at

Lesson
├── id (PK)
├── course_id (FK to Course)
├── title
├── description
├── content
├── order
├── created_at
└── updated_at

Assignment
├── id (PK)
├── course_id (FK to Course)
├── title
├── description
├── due_date
├── points
├── created_at
└── updated_at

Submission
├── id (PK)
├── assignment_id (FK to Assignment)
├── student_id (FK to CustomUser)
├── submission_text
├── status (draft, submitted, graded, returned)
├── grade (0-100, nullable)
├── feedback
├── submitted_at
├── graded_by_id (FK to CustomUser)
├── graded_at
├── created_at
└── updated_at

Enrollment
├── id (PK)
├── student_id (FK to CustomUser)
├── course_id (FK to Course)
├── completed
├── completed_at
└── enrolled_at
```

---

## Settings Configuration

### Important Settings (project/settings.py)

```python
# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'PAGE_SIZE': 10,
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'
```

---

## Future Improvements

### Planned Features

1. **File Upload for Assignments**
   - Support for document uploads
   - Multiple file types (PDF, DOC, Images)
   - File size validation

2. **Email Notifications**
   - Assignment due date reminders
   - Submission confirmation emails
   - Grade notification emails
   - Course enrollment confirmations

3. **Dashboard with Analytics**
   - Student progress dashboard
   - Course completion statistics
   - Grade distribution charts
   - Attendance tracking

4. **Advanced Grading System**
   - Rubric-based grading
   - Percentage-based grades
   - Grade curves
   - Export grades to CSV

5. **Discussion Forums**
   - Course-specific discussion boards
   - Threaded conversations
   - Instructor monitoring
   - Student interaction tracking

6. **Mobile App**
   - React Native/Flutter mobile app
   - Push notifications
   - Offline access to lessons
   - Mobile submission

7. **Payment Integration**
   - Stripe/PayPal integration
   - Course pricing
   - Student payment tracking
   - Refund management

8. **Cloud Deployment**
   - Deployment to Render
   - Deployment to Railway
   - AWS deployment configuration
   - Database backups

9. **Video Hosting**
   - Embed video lessons
   - Video streaming
   - Lecture recordings
   - Download capabilities

10. **Advanced Search & Filtering**
    - Full-text search
    - Course categories
    - Instructor filtering
    - Level filtering

---

## Troubleshooting

### Common Issues

#### **Issue: "Module not found" error**
**Solution**: Make sure you're in the virtual environment and all dependencies are installed.
```bash
pip install -r requirements.txt
```

#### **Issue: Database migration errors**
**Solution**: Clear migrations and run fresh:
```bash
python manage.py migrate --fake courses 0001
python manage.py migrate courses
```

#### **Issue: Port 8000 already in use**
**Solution**: Use a different port:
```bash
python manage.py runserver 8001
```

#### **Issue: Static files not loading**
**Solution**: Collect static files:
```bash
python manage.py collectstatic --noinput
```

#### **Issue: CORS errors in frontend**
**Solution**: Check `CORS_ALLOWED_ORIGINS` in settings.py and add your client URL.

#### **Issue: JWT token expired**
**Solution**: Use the refresh token endpoint to get a new access token:
```
POST /users/api/token/refresh/
```

---

## Development Workflow

### Adding a New Feature

1. **Create Model** (if needed)
   ```bash
   # Edit models.py
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create Serializer**
   - Add to serializers.py

3. **Create ViewSet**
   - Add to views.py
   - Implement permissions

4. **Register in Admin** (if applicable)
   - Add to admin.py

5. **Update URLs**
   - Register router in urls.py

6. **Create Tests**
   - Add test cases

7. **Update Documentation**
   - Update this README

---

## Project Structure

```
final_lms_project/
├── project/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── users/
│   ├── models.py            # CustomUser model
│   ├── views.py             # User views & API views
│   ├── serializers.py       # User serializers
│   ├── urls.py              # User URLs
│   ├── forms.py             # User forms
│   ├── admin.py             # Admin configuration
│   └── migrations/
├── courses/
│   ├── models.py            # Course, Lesson, Assignment, Submission models
│   ├── views.py             # Course views & API views
│   ├── serializers.py       # Course serializers
│   ├── urls.py              # Course URLs
│   ├── admin.py             # Admin configuration
│   ├── management/
│   │   └── commands/
│   │       └── populate_test_data.py  # Test data command
│   └── migrations/
├── templates/               # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── course_list.html
│   ├── my_courses.html
│   ├── create_course.html
│   ├── assignments.html
│   ├── assignment_submit.html
│   ├── view_submissions.html
│   ├── grade_submission.html
│   ├── submission_detail.html
│   └── certificate.html
├── static/
│   └── css/
│       └── style.css        # Enhanced styling
├── certificates/            # Certificate management app
├── manage.py
├── db.sqlite3              # SQLite database
└── requirements.txt        # Python dependencies
```

---

## Contributing

To contribute to this project:

1. Create a new branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request
5. Update documentation

---

## License

This project is open source and available under the MIT License.

---

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

## Version History

- **v1.0.0** (Current) - Initial complete implementation with all core features
  - JWT authentication
  - Role-based access control
  - Course management
  - Assignment submission and grading
  - API with documentation
  - Test data seeding

---

## Author

Created as part of a comprehensive Learning Management System project.

---

**Last Updated:** February 18, 2026
