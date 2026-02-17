
from django.db import models
from django.conf import settings
class Course(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    teacher=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self): return self.title
class Enrollment(models.Model):
    student=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    completed=models.BooleanField(default=False)
