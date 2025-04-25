from django.db import models
from django.contrib.auth.models import User
import datetime


class ClassRoutine(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    day = models.CharField(max_length=10, choices=[
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.day} from {self.start_time} to {self.end_time} in {self.location}"

class ExamRoutine(models.Model):
    course_name = models.CharField(max_length=100, default="Untitled Exam")
    exam_date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.course_name} on {self.exam_date}"


class MyNote(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='mynotes/', blank=True, null=True)
    memory_prompt = models.CharField(max_length=255, blank=True, null=True)
    attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
