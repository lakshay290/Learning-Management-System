from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('create-course/', views.create_course, name='create_course'),
    path('delete-course/<int:id>/', views.delete_course, name='delete_course'),
    path('enroll/<int:id>/', views.enroll, name='enroll'),
    path('complete/<int:id>/', views.complete, name='complete'),
]
