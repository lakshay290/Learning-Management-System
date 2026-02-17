🎓 LMS – Learning Management System

A modern Learning Management System built using Django (Python).
This system allows teachers to create and manage courses, and students to enroll and complete them.

🚀 Features
👨‍🏫 Teacher

Create new courses

Delete courses

View all available courses

👨‍🎓 Student

View all courses

Enroll in courses

View enrolled courses

Mark courses as completed

Generate certificate after completion

🔐 Authentication

User Registration

Login & Logout

Role-based access (Teacher / Student)

🛠 Tech Stack

Backend: Django 5.x

Frontend: HTML, CSS, Bootstrap

Database: SQLite3

Language: Python 3.11

📂 Project Structure
final_lms_project/
│
├── project/              # Main project folder
├── users/                # Authentication app
├── courses/              # Course management app
├── certificates/         # Certificate generation app
├── templates/            # HTML templates
├── static/               # CSS & static files
├── db.sqlite3
└── manage.py

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/lakshay290/Learning-Management-System
cd lms-project

2️⃣ Create Virtual Environment
python -m venv venv


Activate:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3️⃣ Install Dependencies
pip install django

4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Run Server
python manage.py runserver


Open in browser:

http://127.0.0.1:8000/

👤 User Roles
Role	Permissions
Teacher	Create & Delete Courses
Student	Enroll & Complete Courses
📸 Screenshots

Home Page

Course List

Teacher Dashboard

Student Dashboard

(You can add screenshots here)

📜 Future Improvements

Admin dashboard

Course videos upload

Payment integration

Email notifications

Deployment on cloud (AWS / Render)

📄 License

This project is created for educational purposes.

👨‍💻 Author

Lakshay Bishnoi
B.Tech CSE Student
