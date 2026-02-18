from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from courses.models import Course, Lesson, Assignment, Submission, Enrollment

CustomUser = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate test data...')
        
        # Create test users
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@lms.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('password')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        teacher_user, created = CustomUser.objects.get_or_create(
            username='teacher',
            defaults={
                'email': 'teacher@lms.com',
                'role': 'instructor',
                'is_teacher': True,
            }
        )
        if created:
            teacher_user.set_password('password')
            teacher_user.save()
            self.stdout.write(self.style.SUCCESS('Created teacher user'))
        
        student_user, created = CustomUser.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@lms.com',
                'role': 'student',
            }
        )
        if created:
            student_user.set_password('password')
            student_user.save()
            self.stdout.write(self.style.SUCCESS('Created student user'))
        
        # Create test courses
        course1, created = Course.objects.get_or_create(
            title='Introduction to Python',
            defaults={
                'description': 'Learn the basics of Python programming',
                'teacher': teacher_user,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created course: Introduction to Python'))
        
        course2, created = Course.objects.get_or_create(
            title='Web Development with Django',
            defaults={
                'description': 'Master Django for web development',
                'teacher': teacher_user,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created course: Web Development with Django'))
        
        # Create lessons
        lesson1, created = Lesson.objects.get_or_create(
            course=course1,
            title='Getting Started with Python',
            defaults={
                'description': 'Introduction to Python',
                'content': 'Python is a versatile programming language...',
                'order': 1,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created lesson: Getting Started with Python'))
        
        # Create assignments
        assignment1, created = Assignment.objects.get_or_create(
            course=course1,
            title='Hello World Program',
            defaults={
                'description': 'Write a simple Hello World program in Python',
                'due_date': timezone.now() + timedelta(days=7),
                'points': 10,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created assignment: Hello World Program'))
        
        assignment2, created = Assignment.objects.get_or_create(
            course=course2,
            title='Create a Django App',
            defaults={
                'description': 'Create your first Django application',
                'due_date': timezone.now() + timedelta(days=14),
                'points': 50,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created assignment: Create a Django App'))
        
        # Enroll student in courses
        enrollment1, created = Enrollment.objects.get_or_create(
            student=student_user,
            course=course1,
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Enrolled student in: Introduction to Python'))
        
        enrollment2, created = Enrollment.objects.get_or_create(
            student=student_user,
            course=course2,
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Enrolled student in: Web Development with Django'))
        
        # Create a sample submission
        submission1, created = Submission.objects.get_or_create(
            assignment=assignment1,
            student=student_user,
            defaults={
                'submission_text': 'print("Hello World")',
                'content': 'print("Hello World")',
                'status': 'submitted',
                'submitted_at': timezone.now(),
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created sample submission'))
        
        # Grade the submission
        if submission1.grade is None:
            submission1.grade = 10
            submission1.feedback = 'Great work! Perfect Hello World program.'
            submission1.status = 'graded'
            submission1.graded_by = teacher_user
            submission1.graded_at = timezone.now()
            submission1.save()
            self.stdout.write(self.style.SUCCESS('Graded sample submission'))
        
        self.stdout.write(self.style.SUCCESS('Test data population completed successfully!'))
        self.stdout.write('\nTest Credentials:')
        self.stdout.write('Admin: admin / password')
        self.stdout.write('Instructor: teacher / password')
        self.stdout.write('Student: student / password')
