from rest_framework import serializers
from .models import Course, Lesson, Assignment, Submission, Enrollment

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'description', 'content', 'order', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'course', 'title', 'description', 'due_date', 'points', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SubmissionSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)
    graded_by_username = serializers.CharField(source='graded_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'student', 'student_username', 'content', 'submission_text',
            'status', 'submitted_at', 'grade', 'feedback', 'graded_at', 'graded_by', 'graded_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'graded_at', 'submitted_at']

class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'teacher_name', 'lessons', 'assignments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CourseListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)
    lessons_count = serializers.SerializerMethodField()
    assignments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'teacher_name', 'lessons_count', 'assignments_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()
    
    def get_assignments_count(self, obj):
        return obj.assignments.count()

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_username', 'course', 'course_title', 'completed', 'completed_at', 'enrolled_at']
        read_only_fields = ['id', 'enrolled_at', 'completed_at']

class GradeSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for grading submissions"""
    class Meta:
        model = Submission
        fields = ['id', 'grade', 'feedback', 'status']
    
    def update(self, instance, validated_data):
        instance.grade = validated_data.get('grade', instance.grade)
        instance.feedback = validated_data.get('feedback', instance.feedback)
        instance.status = 'graded'
        instance.save()
        return instance

class StudentAssignmentProgressSerializer(serializers.Serializer):
    """Serializer for tracking student progress on assignments"""
    assignment_id = serializers.IntegerField()
    title = serializers.CharField()
    due_date = serializers.DateTimeField()
    status = serializers.CharField()
    grade = serializers.IntegerField(allow_null=True)
    submitted_at = serializers.DateTimeField(allow_null=True)
