from django.shortcuts import render
from users.models import Workshop, Course
from django.contrib.auth.models import User

def home(request):
    workshops = Workshop.objects.all().order_by('-date')
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'main/index.html', {'workshops': workshops, 'courses': courses,})

