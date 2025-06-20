from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')

# Render register page and handle POST request
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password,email=email)
        user.save()
        messages.success(request, 'Registration successful! You can now log in.')

    return render(request, 'users/register.html')


# Render login page and handle POST request
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # 👈 Redirects to homepage
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'users/login.html')


# Handle logout
def logout_view(request):
    logout(request)
    return redirect('login')

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_description = request.POST.get('course_description')
        instructor = request.POST.get('instructor')
        price = request.POST.get('price')
        # Here you would typically save the course to the database
        Course.objects.create(
            title=course_name,
            description=course_description,
            instructor=instructor,
            price=price
        )
        messages.success(request, f'Course "{course_name}" added successfully!')
        return redirect('dashboard')

    return render(request, 'users/add_course.html')