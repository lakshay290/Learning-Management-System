# LMS API Documentation

## Authentication

All API endpoints (except registration) require authentication using JWT tokens.

### Getting an Access Token

1. **Register a new user:**
```bash
curl -X POST http://localhost:8000/users/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "role": "student"
  }'
```

2. **Login to get tokens:**
```bash
curl -X POST http://localhost:8000/users/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

3. **Include the access token in all requests:**
```bash
curl http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## API Endpoints Reference

### User Endpoints

#### POST /users/api/register/
Register a new user

**Request:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  "password_confirm": "password123",
  "role": "student",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201):**
```json
{
  "id": 4,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student"
}
```

#### POST /users/api/token/
Obtain JWT token pair

**Request:**
```json
{
  "username": "student",
  "password": "password"
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "username": "student",
  "email": "student@lms.com",
  "role": "student",
  "is_teacher": false
}
```

#### POST /users/api/token/refresh/
Refresh an expired access token

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### GET /users/api/me/
Get current user's profile

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "id": 3,
  "username": "student",
  "email": "student@lms.com",
  "first_name": "Student",
  "last_name": "User",
  "role": "student",
  "is_teacher": false,
  "is_staff": false,
  "date_joined": "2026-02-18T10:00:00Z"
}
```

#### POST /users/api/change_password/
Change user's password

**Request:**
```json
{
  "old_password": "oldpassword",
  "new_password": "newpassword123",
  "new_password_confirm": "newpassword123"
}
```

**Response (200):**
```json
{
  "detail": "Password changed successfully"
}
```

---

### Course Endpoints

#### GET /api/courses/
List all courses with pagination and search

**Query Parameters:**
- `search` - Search by title or description
- `ordering` - Order by `created_at` or `title`
- `page` - Page number (default: 1)

**Example:**
```bash
curl http://localhost:8000/api/courses/?search=python&ordering=-created_at \
  -H "Authorization: Bearer {token}"
```

**Response (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Python",
      "description": "Learn Python basics",
      "teacher": 2,
      "teacher_name": "teacher",
      "lessons_count": 1,
      "assignments_count": 1,
      "created_at": "2026-02-17T10:00:00Z"
    }
  ]
}
```

#### POST /api/courses/
Create a new course (Instructor only)

**Request:**
```json
{
  "title": "Advanced Python",
  "description": "Learn advanced Python concepts"
}
```

**Response (201):**
```json
{
  "id": 3,
  "title": "Advanced Python",
  "description": "Learn advanced Python concepts",
  "teacher": 2,
  "teacher_name": "teacher",
  "lessons": [],
  "assignments": [],
  "created_at": "2026-02-18T15:20:00Z",
  "updated_at": "2026-02-18T15:20:00Z"
}
```

#### GET /api/courses/{id}/
Get course details with lessons and assignments

**Response (200):**
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "description": "Learn Python basics",
  "teacher": 2,
  "teacher_name": "teacher",
  "lessons": [
    {
      "id": 1,
      "course": 1,
      "title": "Getting Started",
      "description": "Intro to Python",
      "content": "Python is...",
      "order": 1,
      "created_at": "2026-02-17T10:00:00Z",
      "updated_at": "2026-02-17T10:00:00Z"
    }
  ],
  "assignments": [
    {
      "id": 1,
      "course": 1,
      "title": "Hello World",
      "description": "Write Hello World",
      "due_date": "2026-03-01T23:59:59Z",
      "points": 10,
      "created_at": "2026-02-17T10:00:00Z",
      "updated_at": "2026-02-17T10:00:00Z"
    }
  ],
  "created_at": "2026-02-17T10:00:00Z",
  "updated_at": "2026-02-17T10:00:00Z"
}
```

#### POST /api/courses/{id}/enroll/
Enroll student in a course

**Response (201 or 200):**
```json
{
  "detail": "Enrolled successfully"
}
```

#### GET /api/courses/{id}/check_enrollment/
Check if user is enrolled in course

**Response (200):**
```json
{
  "enrolled": true
}
```

#### POST /api/courses/{id}/assign_student/
Assign a student to a course (Instructor only)

**Request:**
```json
{
  "student_id": 3
}
```

**Response (201 or 200):**
```json
{
  "id": 1,
  "student": 3,
  "student_username": "student",
  "course": 1,
  "course_title": "Introduction to Python",
  "completed": false,
  "completed_at": null,
  "enrolled_at": "2026-02-18T09:00:00Z"
}
```

**Errors:**
- 403: Only course teacher can assign students
- 404: Student not found

---

### Lesson Endpoints

#### GET /api/lessons/
List all lessons (filter by course_id)

**Query Parameters:**
- `course_id` - Filter by course ID
- `ordering` - Order by `order` or `created_at`

**Example:**
```bash
curl http://localhost:8000/api/lessons/?course_id=1 \
  -H "Authorization: Bearer {token}"
```

**Response (200):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "course": 1,
      "title": "Getting Started with Python",
      "description": "Introduction",
      "content": "Python is a versatile...",
      "order": 1,
      "created_at": "2026-02-17T10:00:00Z",
      "updated_at": "2026-02-17T10:00:00Z"
    }
  ]
}
```

#### POST /api/lessons/
Create a new lesson (Instructor only)

**Request:**
```json
{
  "course": 1,
  "title": "Functions in Python",
  "description": "Learn about functions",
  "content": "A function is a reusable block...",
  "order": 2
}
```

**Response (201):**
```json
{
  "id": 2,
  "course": 1,
  "title": "Functions in Python",
  "description": "Learn about functions",
  "content": "A function is a reusable block...",
  "order": 2,
  "created_at": "2026-02-18T11:00:00Z",
  "updated_at": "2026-02-18T11:00:00Z"
}
```

---

### Assignment Endpoints

#### GET /api/assignments/
List all assignments (filter by course_id)

**Query Parameters:**
- `course_id` - Filter by course ID
- `ordering` - Order by `due_date` or `created_at`

**Response (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "course": 1,
      "title": "Hello World Program",
      "description": "Write Hello World",
      "due_date": "2026-03-01T23:59:59Z",
      "points": 10,
      "created_at": "2026-02-17T10:00:00Z",
      "updated_at": "2026-02-17T10:00:00Z"
    }
  ]
}
```

#### POST /api/assignments/
Create a new assignment (Instructor only)

**Request:**
```json
{
  "course": 1,
  "title": "Assignment 2",
  "description": "Write a function",
  "due_date": "2026-03-08T23:59:59Z",
  "points": 25
}
```

**Response (201):**
```json
{
  "id": 3,
  "course": 1,
  "title": "Assignment 2",
  "description": "Write a function",
  "due_date": "2026-03-08T23:59:59Z",
  "points": 25,
  "created_at": "2026-02-18T12:00:00Z",
  "updated_at": "2026-02-18T12:00:00Z"
}
```

#### GET /api/assignments/{id}/submissions/
Get all submissions for an assignment (Instructor only)

**Response (200):**
```json
[
  {
    "id": 1,
    "assignment": 1,
    "student": 3,
    "student_username": "student",
    "content": "print('Hello World')",
    "submission_text": "print('Hello World')",
    "status": "graded",
    "submitted_at": "2026-02-18T10:00:00Z",
    "grade": 10,
    "feedback": "Perfect!",
    "graded_at": "2026-02-18T15:00:00Z",
    "graded_by": 2,
    "graded_by_username": "teacher",
    "created_at": "2026-02-18T10:00:00Z",
    "updated_at": "2026-02-18T15:00:00Z"
  }
]
```

#### POST /api/assignments/{id}/assign_student/
Assign an assignment to a student (Instructor only)

**Request:**
```json
{
  "student_id": 3
}
```

**Response (201 or 200):**
```json
{
  "id": 1,
  "assignment": 1,
  "student": 3,
  "student_username": "student",
  "content": "",
  "submission_text": "",
  "status": "draft",
  "submitted_at": null,
  "grade": null,
  "feedback": null,
  "graded_at": null,
  "graded_by": null,
  "graded_by_username": null,
  "created_at": "2026-02-18T10:00:00Z",
  "updated_at": "2026-02-18T10:00:00Z"
}
```

**Errors:**
- 403: Only course instructor can assign
- 404: Student not found

---

### Submission Endpoints

#### GET /api/submissions/
List submissions (based on user role)

**For Students:** Returns their own submissions
**For Instructors:** Returns submissions for their course assignments

**Response (200):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "assignment": 1,
      "student": 3,
      "student_username": "student",
      "content": "print('Hello World')",
      "submission_text": "print('Hello World')",
      "status": "graded",
      "submitted_at": "2026-02-18T10:00:00Z",
      "grade": 10,
      "feedback": "Great work!",
      "graded_at": "2026-02-18T15:00:00Z",
      "graded_by": 2,
      "graded_by_username": "teacher",
      "created_at": "2026-02-18T10:00:00Z",
      "updated_at": "2026-02-18T15:00:00Z"
    }
  ]
}
```

#### POST /api/submissions/
Create or update a submission (Student only)

**Request:**
```json
{
  "assignment": 1,
  "submission_text": "def hello():\n    print('Hello World')\n\nhello()"
}
```

**Response (201):**
```json
{
  "id": 2,
  "assignment": 1,
  "student": 3,
  "student_username": "student",
  "content": "def hello()...",
  "submission_text": "def hello()...",
  "status": "submitted",
  "submitted_at": "2026-02-18T14:00:00Z",
  "grade": null,
  "feedback": "",
  "graded_at": null,
  "graded_by": null,
  "graded_by_username": null,
  "created_at": "2026-02-18T14:00:00Z",
  "updated_at": "2026-02-18T14:00:00Z"
}
```

#### POST /api/submissions/{id}/grade/
Grade a submission with feedback (Instructor only)

**Request:**
```json
{
  "grade": 85,
  "feedback": "Excellent work! Your code is clean and efficient.",
  "status": "graded"
}
```

**Response (200):**
```json
{
  "id": 2,
  "grade": 85,
  "feedback": "Excellent work!",
  "status": "graded"
}
```

#### GET /api/submissions/my_submissions/
Get all of the current student's submissions

**Response (200):**
```json
[
  {
    "id": 1,
    "assignment": 1,
    "student": 3,
    "student_username": "student",
    "status": "graded",
    "grade": 85,
    "submitted_at": "2026-02-18T10:00:00Z"
  }
]
```

#### DELETE /api/submissions/{id}/remove_student/
Remove a student from an assignment (Instructor only)

**Response (204 No Content)**

**Errors:**
- 403: Only course instructor can remove assignments

---

### Enrollment Endpoints

#### GET /api/enrollments/
List all enrollments (filtered by user)

**For Students:** Returns their enrollments
**For Instructors:** Returns enrollments in their courses

**Response (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "student": 3,
      "student_username": "student",
      "course": 1,
      "course_title": "Introduction to Python",
      "completed": false,
      "completed_at": null,
      "enrolled_at": "2026-02-18T09:00:00Z"
    }
  ]
}
```

#### GET /api/enrollments/my_courses/
Get all courses enrolled by current student

**Response (200):**
```json
[
  {
    "id": 1,
    "student": 3,
    "student_username": "student",
    "course": 1,
    "course_title": "Introduction to Python",
    "completed": false,
    "completed_at": null,
    "enrolled_at": "2026-02-18T09:00:00Z"
  }
]
```

#### DELETE /api/enrollments/{id}/remove_student/
Remove a student from a course (Instructor only)

**Response (204 No Content)**

**Errors:**
- 403: Only course teacher can remove students

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

---

## Rate Limiting

Currently, there is no rate limiting configured. It can be added in settings.py:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

---

## Pagination

All list endpoints return paginated results:

```json
{
  "count": 10,
  "next": "http://localhost:8000/api/courses/?page=2",
  "previous": null,
  "results": [...]
}
```

Default page size: 10 items (configurable in settings.py)

---

## Filtering & Search

### Search
Use the `search` parameter on endpoints that support it:
```
GET /api/courses/?search=python
```

### Ordering
Use the `ordering` parameter:
```
GET /api/assignments/?ordering=-due_date
```

Use `-` prefix for descending order.

---

## Testing with cURL

### Get Token
```bash
curl -X POST http://localhost:8000/users/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student","password":"password"}' | jq '.access' -r > token.txt
```

### Use Token in Request
```bash
curl -H "Authorization: Bearer $(cat token.txt)" \
  http://localhost:8000/api/courses/
```

---

## Testing with Postman

1. **Create Collection** - LMS API
2. **Add Environment Variable:**
   - Variable: `token`
   - Value: (leave blank, will be set by script)

3. **Create Request - Get Token:**
   - Method: POST
   - URL: `http://localhost:8000/users/api/token/`
   - Body (raw JSON):
     ```json
     {"username":"student","password":"password"}
     ```
   - Tests tab:
     ```javascript
     var jsonData = pm.response.json();
     pm.environment.set("token", jsonData.access);
     ```

4. **Create Request - List Courses:**
   - Method: GET
   - URL: `http://localhost:8000/api/courses/`
   - Headers: `Authorization: Bearer {{token}}`

---

## Code Examples

### Python Requests
```python
import requests

# Login
response = requests.post(
    'http://localhost:8000/users/api/token/',
    json={'username': 'student', 'password': 'password'}
)
token = response.json()['access']

# Get courses
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(
    'http://localhost:8000/api/courses/',
    headers=headers
)
print(response.json())
```

### JavaScript Fetch
```javascript
// Login
const response = await fetch('http://localhost:8000/users/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'student',
    password: 'password'
  })
});

const { access } = await response.json();

// Get courses
const coursesResponse = await fetch('http://localhost:8000/api/courses/', {
  headers: { 'Authorization': `Bearer ${access}` }
});

const courses = await coursesResponse.json();
console.log(courses);
```

---

## Rate Limits & Best Practices

- Always use HTTPS in production
- Refresh tokens before they expire
- Handle 401 responses to re-authenticate
- Implement pagination for list endpoints
- Cache responses when appropriate
- Use query parameters to filter data
- Validate input before sending requests

---

**Last Updated:** February 18, 2026
