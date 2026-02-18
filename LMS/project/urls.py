from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/docs/', include_docs_urls(title='LMS API Documentation')),

    # Landing Page + Courses
    path('', include('courses.urls')),

    # Users (Login/Register)
    path('users/', include('users.urls')),
    
    # API Auth
    path('api-auth/', include('rest_framework.urls')),
]
