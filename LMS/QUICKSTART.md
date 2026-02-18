# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd "c:\Users\Lakshay Bishnoi\OneDrive\Desktop\study\pep project\final_lms_project"
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Apply Migrations
```bash
python manage.py migrate
```

### Step 3: Create Test Data
```bash
python manage.py populate_test_data
```

This creates 3 test users:
- **Admin**: `admin / password`
- **Instructor**: `teacher / password`
- **Student**: `student / password`

### Step 4: Start Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

---

## Test the System

### Login as Student
1. Go to `http://localhost:8000/users/login/`
2. Username: `student`
3. Password: `password`
4. Click "View All Courses" to see available courses
5. Enroll in a course
6. Go to "My Enrolled Courses" to view assignments

### Login as Instructor
1. Go to `http://localhost:8000/users/login/`
2. Username: `teacher`
3. Password: `password`
4. Create a new course
5. Add lessons and assignments
6. View and grade student submissions

### Access Admin Panel
1. Go to `http://localhost:8000/admin/`
2. Username: `admin`
3. Password: `password`
4. Manage users, courses, assignments, etc.

---

## API Quick Test

### 1. Get Authentication Token
```bash
curl -X POST http://localhost:8000/users/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"student","password":"password"}'
```

Copy the `access` token from response.

### 2. List Courses
```bash
curl http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Create Submission
```bash
curl -X POST http://localhost:8000/api/submissions/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "assignment": 1,
    "submission_text": "print(\"Hello World\")"
  }'
```

---

## Key Files to Edit

### Add New Model
1. Edit `courses/models.py` or `users/models.py`
2. Create serializer in `serializers.py`
3. Create viewset in `views.py`
4. Register in `urls.py`
5. Add to `admin.py`
6. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Modify Styling
- Edit `static/css/style.css`

### Create New Page
1. Create HTML in `templates/`
2. Add view in `views.py`
3. Add URL in `urls.py`

---

## Common Commands

```bash
# Create migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Flush database (delete all data)
python manage.py flush

# Run tests
python manage.py test
```

---

## Project Structure Overview

```
final_lms_project/
├── users/              # User authentication & management
├── courses/            # Courses, lessons, assignments
├── templates/          # HTML files
├── static/             # CSS, JS, images
├── project/            # Django settings
├── manage.py
├── db.sqlite3
├── README.md           # Full documentation
└── API_DOCUMENTATION.md # API reference
```

---

## Next Steps

1. **Deploy to Cloud** - Use Render, Railway, or AWS
2. **Add Email Notifications** - Send assignment reminders
3. **File Uploads** - Allow students to upload documents
4. **Mobile App** - Create React Native/Flutter app
5. **Payment System** - Integrate Stripe for paid courses
6. **Video Hosting** - Embed YouTube or add video lessons

---

## Troubleshooting

**Port already in use?**
```bash
python manage.py runserver 8001
```

**Database error?**
```bash
python manage.py migrate --fake courses 0001
python manage.py migrate
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

**Need to reset everything?**
```bash
python manage.py flush
python manage.py populate_test_data
```

---

## Getting Help

- Read full docs: [README.md](README.md)
- API Reference: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Admin Panel: `http://localhost:8000/admin/`
- API Docs: `http://localhost:8000/api/docs/`

---

Happy Learning! 🚀
