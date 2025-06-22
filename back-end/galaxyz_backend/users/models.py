from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    instructor = models.CharField(max_length=100)
    numberOfRegisteredUsers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    poster = models.ImageField(upload_to='course_posters/', null=True, blank=True)
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    courseVideoLink = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Workshop(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    duration = models.DurationField()
    meetLink = models.URLField(max_length=200, null=True, blank=True)
    instructor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    poster = models.ImageField(upload_to='workshop_posters/', null=True, blank=True)
    registeredParticipants = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.course.title}"
