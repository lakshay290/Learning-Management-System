from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Course, Enrollment, Lesson, Assignment, Submission
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    LessonSerializer,
    AssignmentSerializer,
    SubmissionSerializer,
    EnrollmentSerializer,
    GradeSubmissionSerializer
)

# ==================== TRADITIONAL VIEWS ====================

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
    enrollment.completed_at = timezone.now()
    enrollment.save()

    return redirect('my_courses')


# ================= ASSIGNMENTS =================
@login_required
def view_assignments(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = course.assignments.all()

    return render(request, 'assignments.html', {
        'assignments': assignments,
        'course': course
    })


# ================= SUBMIT ASSIGNMENT =================
@login_required
def submit_assignment(request, id):
    if request.user.is_teacher:
        return redirect('home')

    assignment = get_object_or_404(Assignment, id=id)
    submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    if request.method == "POST":
        submission_text = request.POST.get('submission_text')
        
        if submission:
            submission.submission_text = submission_text
            submission.status = 'submitted'
            submission.submitted_at = timezone.now()
            submission.save()
        else:
            Submission.objects.create(
                assignment=assignment,
                student=request.user,
                submission_text=submission_text,
                content=submission_text,
                status='submitted',
                submitted_at=timezone.now()
            )
        
        return redirect('my_courses')

    return render(request, 'assignment_submit.html', {
        'assignment': assignment,
        'submission': submission
    })


# ================= VIEW SUBMISSIONS (TEACHER) =================
@login_required
def view_submissions(request, id):
    if not request.user.is_teacher:
        return redirect('home')

    assignment = get_object_or_404(Assignment, id=id)

    if assignment.course.teacher != request.user:
        return redirect('home')

    submissions = assignment.submissions.all()

    return render(request, 'view_submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })


# ================= GRADE SUBMISSION (TEACHER) =================
@login_required
def grade_submission(request, id):
    submission = get_object_or_404(Submission, id=id)

    if submission.assignment.course.teacher != request.user:
        return redirect('home')

    if request.method == "POST":
        grade = request.POST.get('grade')
        feedback = request.POST.get('feedback')

        if grade:
            try:
                grade_int = int(grade)
                if 0 <= grade_int <= 100:
                    submission.grade = grade_int
                    submission.feedback = feedback
                    submission.status = 'graded'
                    submission.graded_by = request.user
                    submission.graded_at = timezone.now()
                    submission.save()
                    return redirect('view_submissions', id=submission.assignment.id)
                else:
                    return render(request, 'grade_submission.html', {
                        'submission': submission,
                        'error': 'Grade must be between 0 and 100'
                    })
            except ValueError:
                return render(request, 'grade_submission.html', {
                    'submission': submission,
                    'error': 'Grade must be a valid number'
                })

    return render(request, 'grade_submission.html', {
        'submission': submission
    })


# ================= VIEW SUBMISSION DETAIL =================
@login_required
def view_submission_detail(request, id):
    submission = get_object_or_404(Submission, id=id)

    # Check permissions
    if ((submission.student != request.user and 
         submission.assignment.course.teacher != request.user and 
         not request.user.is_staff)):
        return redirect('home')

    return render(request, 'submission_detail.html', {
        'submission': submission
    })


# ================= CREATE ASSIGNMENT (TEACHER) =================
@login_required
def create_assignment(request, course_id):
    """Teacher can create assignment for a course"""
    if not request.user.is_teacher:
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id)
    
    # Verify teacher owns the course
    if course.teacher != request.user:
        return redirect('home')
    
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        points = request.POST.get('points', 0)
        
        Assignment.objects.create(
            course=course,
            title=title,
            description=description,
            due_date=due_date if due_date else None,
            points=int(points) if points else 0
        )
        return redirect('manage_assignments')
    
    return render(request, 'create_assignment.html', {
        'course': course
    })


# ================= DELETE ASSIGNMENT (TEACHER) =================
@login_required
def delete_assignment(request, assignment_id):
    """Teacher can delete an assignment"""
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Verify teacher owns the course
    if assignment.course.teacher != request.user:
        return redirect('home')
    
    assignment.delete()
    return redirect('manage_assignments')


# ================= TEACHER: MANAGE ASSIGNMENTS =================
@login_required
def manage_assignments(request):
    """Teacher can assign assignments to students"""
    if not request.user.is_teacher:
        return redirect('home')
    
    # Get courses taught by this teacher
    courses = Course.objects.filter(teacher=request.user)
    teacher_assignments = Assignment.objects.filter(course__teacher=request.user)
    
    return render(request, 'manage_assignments.html', {
        'courses': courses,
        'assignments': teacher_assignments
    })


# ================= TEACHER: ASSIGN STUDENT TO ASSIGNMENT =================
@login_required
def assign_student_to_assignment(request, assignment_id):
    """Allow teacher to assign assignment to specific students"""
    if not request.user.is_teacher:
        return redirect('home')
    
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Verify teacher owns the course
    if assignment.course.teacher != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            from django.contrib.auth import get_user_model
            CustomUser = get_user_model()
            student = get_object_or_404(CustomUser, id=student_id, role='student')
            
            # Create submission for the student
            submission, created = Submission.objects.get_or_create(
                assignment=assignment,
                student=student,
                defaults={
                    'content': '',
                    'submission_text': '',
                    'status': 'draft'
                }
            )
        
        return redirect('assign_student_to_assignment', assignment_id=assignment_id)
    
    # Get all students not yet assigned to this assignment
    from django.contrib.auth import get_user_model
    CustomUser = get_user_model()
    
    all_students = CustomUser.objects.filter(role='student')
    assigned_students = Submission.objects.filter(
        assignment=assignment
    ).values_list('student_id', flat=True)
    
    available_students = all_students.exclude(id__in=assigned_students)
    assigned_submissions = Submission.objects.filter(assignment=assignment)
    
    return render(request, 'assign_student_to_assignment.html', {
        'assignment': assignment,
        'available_students': available_students,
        'assigned_submissions': assigned_submissions
    })


# ================= TEACHER: ASSIGN STUDENT TO COURSE =================
@login_required
def enroll_student_to_course(request, course_id):
    """Allow teacher to enroll students to their course"""
    if not request.user.is_teacher:
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id)
    
    # Verify teacher owns the course
    if course.teacher != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            from django.contrib.auth import get_user_model
            CustomUser = get_user_model()
            student = get_object_or_404(CustomUser, id=student_id, role='student')
            
            # Enroll the student
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                course=course
            )
        
        return redirect('enroll_student_to_course', course_id=course_id)
    
    # Get all students not enrolled in this course
    from django.contrib.auth import get_user_model
    CustomUser = get_user_model()
    
    all_students = CustomUser.objects.filter(role='student')
    enrolled_students = Enrollment.objects.filter(
        course=course
    ).values_list('student_id', flat=True)
    
    available_students = all_students.exclude(id__in=enrolled_students)
    current_enrollments = Enrollment.objects.filter(course=course)
    
    return render(request, 'enroll_student_to_course.html', {
        'course': course,
        'available_students': available_students,
        'current_enrollments': current_enrollments
    })


# ================= TEACHER: REMOVE STUDENT FROM COURSE =================
@login_required
def remove_student_from_course(request, enrollment_id):
    """Remove student from course"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    # Verify teacher owns the course
    if enrollment.course.teacher != request.user:
        return redirect('home')
    
    course_id = enrollment.course.id
    enrollment.delete()
    
    return redirect('enroll_student_to_course', course_id=course_id)


# ================= TEACHER: REMOVE ASSIGNMENT FROM STUDENT =================
@login_required
def remove_assignment_from_student(request, submission_id):
    """Remove assignment from student"""
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Verify teacher owns the course
    if submission.assignment.course.teacher != request.user:
        return redirect('home')
    
    assignment_id = submission.assignment.id
    submission.delete()
    
    return redirect('assign_student_to_assignment', assignment_id=assignment_id)


# ================= STUDENT: VIEW ASSIGNED ASSIGNMENTS =================
@login_required
def my_assignments(request):
    """View assignments assigned to student"""
    if request.user.is_teacher:
        return redirect('home')
    
    # Get all assignments assigned to this student (where submission exists)
    submissions = Submission.objects.filter(student=request.user).select_related('assignment__course')
    
    # Group by course
    assignments_by_course = {}
    for submission in submissions:
        course = submission.assignment.course
        if course.id not in assignments_by_course:
            assignments_by_course[course.id] = {
                'course': course,
                'assignments': []
            }
        assignments_by_course[course.id]['assignments'].append(submission)
    
    return render(request, 'my_assignments.html', {
        'assignments_by_course': assignments_by_course.values()
    })


# ==================== API VIEWSETS ====================

class CourseViewSet(viewsets.ModelViewSet):
    """Course management API"""
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Ensure only instructors can create courses
        if self.request.user.role in ['instructor', 'admin']:
            serializer.save(teacher=self.request.user)
        else:
            return Response({'detail': 'Only instructors can create courses'}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        """Enroll a student in a course"""
        course = self.get_object()
        if request.user.is_teacher:
            return Response({'detail': 'Teachers cannot enroll in courses'}, status=status.HTTP_400_BAD_REQUEST)
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course
        )
        
        if created:
            return Response({'detail': 'Enrolled successfully'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Already enrolled'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def check_enrollment(self, request, pk=None):
        """Check if user is enrolled in a course"""
        course = self.get_object()
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
        return Response({'enrolled': is_enrolled})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assign_student(self, request, pk=None):
        """Teacher assigns a student to a course"""
        course = self.get_object()
        
        # Ensure user is the course teacher
        if course.teacher != request.user and not request.user.is_staff:
            return Response({'detail': 'Only course teacher can assign students'}, status=status.HTTP_403_FORBIDDEN)
        
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({'detail': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.auth import get_user_model
        CustomUser = get_user_model()
        try:
            student = CustomUser.objects.get(id=student_id, role='student')
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course
        )
        
        serializer = EnrollmentSerializer(enrollment)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class LessonViewSet(viewsets.ModelViewSet):
    """Lesson management API"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Lesson.objects.filter(course_id=course_id)
        return Lesson.objects.all()
    
    def perform_create(self, serializer):
        # Ensure only course instructor can create lessons
        course = Course.objects.get(id=serializer.validated_data['course'].id)
        if self.request.user == course.teacher or self.request.user.is_staff:
            serializer.save()
        else:
            return Response({'detail': 'Only course instructor can create lessons'}, status=status.HTTP_403_FORBIDDEN)


class AssignmentViewSet(viewsets.ModelViewSet):
    """Assignment management API"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['-due_date']
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Assignment.objects.filter(course_id=course_id)
        return Assignment.objects.all()
    
    def perform_create(self, serializer):
        # Ensure only course instructor can create assignments
        course = Course.objects.get(id=serializer.validated_data['course'].id)
        if self.request.user == course.teacher or self.request.user.is_staff:
            serializer.save()
        else:
            return Response({'detail': 'Only course instructor can create assignments'}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def submissions(self, request, pk=None):
        """Get all submissions for an assignment"""
        assignment = self.get_object()
        submissions = assignment.submissions.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assign_student(self, request, pk=None):
        """Assign assignment to a student"""
        assignment = self.get_object()
        
        # Ensure user is the course instructor
        if assignment.course.teacher != request.user and not request.user.is_staff:
            return Response({'detail': 'Only course instructor can assign'}, status=status.HTTP_403_FORBIDDEN)
        
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({'detail': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.auth import get_user_model
        CustomUser = get_user_model()
        try:
            student = CustomUser.objects.get(id=student_id, role='student')
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        submission, created = Submission.objects.get_or_create(
            assignment=assignment,
            student=student,
            defaults={
                'content': '',
                'submission_text': '',
                'status': 'draft'
            }
        )
        
        serializer = SubmissionSerializer(submission)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class SubmissionViewSet(viewsets.ModelViewSet):
    """Submission management API"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['submitted_at', 'grade']
    ordering = ['-submitted_at']
    
    def get_queryset(self):
        # Students see only their submissions
        # Teachers see submissions for their courses
        if self.request.user.is_teacher or self.request.user.is_staff:
            return Submission.objects.filter(assignment__course__teacher=self.request.user)
        return Submission.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        # Ensure only the assigned student can submit
        serializer.save(student=self.request.user, status='submitted', submitted_at=timezone.now())
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def grade(self, request, pk=None):
        """Grade a submission"""
        submission = self.get_object()
        
        # Ensure user is the course instructor
        if submission.assignment.course.teacher != request.user and not request.user.is_staff:
            return Response({'detail': 'Only course instructor can grade'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = GradeSubmissionSerializer(submission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(graded_by=request.user, graded_at=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_submissions(self, request):
        """Get all submissions of the current student"""
        submissions = Submission.objects.filter(student=request.user)
        serializer = self.get_serializer(submissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_student(self, request, pk=None):
        """Remove a student from an assignment"""
        submission = self.get_object()
        
        # Ensure user is the course teacher
        if submission.assignment.course.teacher != request.user and not request.user.is_staff:
            return Response({'detail': 'Only course instructor can remove assignments'}, status=status.HTTP_403_FORBIDDEN)
        
        submission.delete()
        return Response({'detail': 'Assignment removed from student'}, status=status.HTTP_204_NO_CONTENT)


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """Enrollment management API"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['enrolled_at', 'completed_at']
    ordering = ['-enrolled_at']
    
    def get_queryset(self):
        # Students see only their enrollments
        # Teachers see enrollments in their courses
        if self.request.user.is_teacher or self.request.user.is_staff:
            return Enrollment.objects.filter(course__teacher=self.request.user)
        return Enrollment.objects.filter(student=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_courses(self, request):
        """Get all enrolled courses of the current student"""
        enrollments = Enrollment.objects.filter(student=request.user)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_student(self, request, pk=None):
        """Remove a student from a course"""
        enrollment = self.get_object()
        
        # Ensure user is the course teacher
        if enrollment.course.teacher != request.user and not request.user.is_staff:
            return Response({'detail': 'Only course teacher can remove students'}, status=status.HTTP_403_FORBIDDEN)
        
        enrollment.delete()
        return Response({'detail': 'Student removed successfully'}, status=status.HTTP_204_NO_CONTENT)

