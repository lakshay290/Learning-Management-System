from django.contrib import admin
from .models import Course, Lesson, Assignment, Submission, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    list_filter = ('teacher', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {'fields': ('title', 'description', 'teacher')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {'fields': ('course', 'title', 'description', 'content', 'order')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'points', 'created_at')
    list_filter = ('course', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {'fields': ('course', 'title', 'description', 'points')}),
        ('Due Date', {'fields': ('due_date',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'status', 'grade', 'submitted_at', 'graded_at')
    list_filter = ('status', 'submitted_at', 'graded_at', 'assignment__course')
    search_fields = ('student__username', 'assignment__title')
    readonly_fields = ('created_at', 'updated_at', 'submitted_at', 'graded_at')
    fieldsets = (
        ('Assignment Info', {'fields': ('assignment', 'student')}),
        ('Submission Content', {'fields': ('submission_text', 'content')}),
        ('Grading', {'fields': ('status', 'grade', 'feedback', 'graded_by', 'graded_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'submitted_at'), 'classes': ('collapse',)}),
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'completed', 'enrolled_at', 'completed_at')
    list_filter = ('course', 'completed', 'enrolled_at')
    search_fields = ('student__username', 'course__title')
    readonly_fields = ('enrolled_at', 'completed_at')
    fieldsets = (
        ('Enrollment Details', {'fields': ('student', 'course')}),
        ('Status', {'fields': ('completed', 'completed_at')}),
        ('Timestamps', {'fields': ('enrolled_at',), 'classes': ('collapse',)}),
    )
