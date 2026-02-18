from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/courses', views.CourseViewSet, basename='course')
router.register(r'api/lessons', views.LessonViewSet, basename='lesson')
router.register(r'api/assignments', views.AssignmentViewSet, basename='assignment')
router.register(r'api/submissions', views.SubmissionViewSet, basename='submission')
router.register(r'api/enrollments', views.EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    # Traditional views
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-assignments/', views.my_assignments, name='my_assignments'),
    path('create-course/', views.create_course, name='create_course'),
    path('delete-course/<int:id>/', views.delete_course, name='delete_course'),
    path('enroll/<int:id>/', views.enroll, name='enroll'),
    path('complete/<int:id>/', views.complete, name='complete'),
    
    # Assignments
    path('course/<int:course_id>/assignments/', views.view_assignments, name='view_assignments'),
    path('course/<int:course_id>/create-assignment/', views.create_assignment, name='create_assignment'),
    path('assignment/<int:assignment_id>/delete/', views.delete_assignment, name='delete_assignment'),
    path('assignment/<int:id>/submit/', views.submit_assignment, name='assignment_submit'),
    path('assignment/<int:id>/submissions/', views.view_submissions, name='view_submissions'),
    path('submission/<int:id>/grade/', views.grade_submission, name='grade_submission'),
    path('submission/<int:id>/', views.view_submission_detail, name='view_submission_detail'),
    
    # Teacher Management Features
    path('manage-assignments/', views.manage_assignments, name='manage_assignments'),
    path('assignment/<int:assignment_id>/assign-student/', views.assign_student_to_assignment, name='assign_student_to_assignment'),
    path('submission/<int:submission_id>/remove/', views.remove_assignment_from_student, name='remove_assignment_from_student'),
    path('course/<int:course_id>/enroll-student/', views.enroll_student_to_course, name='enroll_student_to_course'),
    path('enrollment/<int:enrollment_id>/remove/', views.remove_student_from_course, name='remove_student_from_course'),
    
    # API routes
    path('', include(router.urls)),
]
