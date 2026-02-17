from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Landing Page + Courses
    path('', include('courses.urls')),

    # Users (Login/Register)
    path('users/', include('users.urls')),
]
