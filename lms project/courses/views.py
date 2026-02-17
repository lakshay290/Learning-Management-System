from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment


# ================= HOME =================
def home(request):
    return render(request, 'home.html')


# ================= COURSE LIST =================
def course_list(request):
    courses = Course.objects.all()

    enrolled_course_ids = []

    if request.user.is_authenticated and not request.user.is_teacher:
        enrolled_course_ids = Enrollment.objects.filter(
            student=request.user
        ).values_list('course_id', flat=True)

    return render(request, 'course_list.html', {
        'courses': courses,
        'enrolled_course_ids': enrolled_course_ids
    })


# ================= MY COURSES (STUDENT) =================
@login_required
def my_courses(request):
    if request.user.is_teacher:
        return redirect('home')

    enrollments = Enrollment.objects.filter(student=request.user)

    return render(request, 'my_courses.html', {
        'enrollments': enrollments
    })


# ================= CREATE COURSE (TEACHER) =================
@login_required
def create_course(request):
    if not request.user.is_teacher:
        return redirect('home')

    if request.method == "POST":
        Course.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            teacher=request.user
        )
        return redirect('home')

    return render(request, 'create_course.html')


# ================= DELETE COURSE (TEACHER) =================
@login_required
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)

    if request.user == course.teacher:
        course.delete()

    return redirect('home')


# ================= ENROLL =================
@login_required
def enroll(request, id):
    if request.user.is_teacher:
        return redirect('home')

    course = get_object_or_404(Course, id=id)

    Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    return redirect('course_list')


# ================= COMPLETE COURSE =================
@login_required
def complete(request, id):
    enrollment = get_object_or_404(
        Enrollment,
        id=id,
        student=request.user
    )

    enrollment.completed = True
    enrollment.save()

    return redirect('my_courses')
