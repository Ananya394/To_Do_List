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


<<<<<<< Updated upstream
class MyNote(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='mynotes/', blank=True, null=True)
    memory_prompt = models.CharField(max_length=255, blank=True, null=True)
    attended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
=======
from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]

    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)  # e.g., Study, Project, Exam
    tags = models.CharField(max_length=100, blank=True)  # comma-separated or use a Tag model
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    duration = models.DurationField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    reminder_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
class ChecklistItem(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='checklist_items')
    description = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} - {'Done' if self.is_done else 'Pending'}"
>>>>>>> Stashed changes
