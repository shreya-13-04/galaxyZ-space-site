from django.shortcuts import render
from users.models import Workshop, Course
from blog.models import Blog
from django.contrib.auth.models import User

def home(request):
    workshops = Workshop.objects.all().order_by('-date')
    courses = Course.objects.all().order_by('-created_at')
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'main/index.html', {'workshops': workshops, 'courses': courses, 'blogs': blogs})

def privacy(request):
    return render(request, 'main/privacy.html')

def terms(request):
    return render(request, 'main/terms.html')
def shipping(request):
    return render(request, 'main/shipping.html')
def refund(request):
    return render(request, 'main/refund_policy.html')


