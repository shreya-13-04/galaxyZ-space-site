from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Workshop, CourseEnrollment, WorkshopRegistration
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import timedelta,datetime

@login_required
def dashboard(request):
    enrollments = CourseEnrollment.objects.filter(user=request.user).select_related('course')
    return render(request, 'users/dashboard.html', {'enrollments': enrollments})

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
        course_description = request.POST.get('description')
        instructor = request.POST.get('instructor')
        price = request.POST.get('price')
        courseVideoLink = request.POST.get('courseVideoLink')
        poster = request.FILES.get('poster')
        pdf = request.FILES.get('pdf')
        # Here you would typically save the course to the database
        Course.objects.create(
            title=course_name,
            description=course_description,
            instructor=instructor,
            price=price,
            courseVideoLink=courseVideoLink,
            poster=poster,
            pdf=pdf
        )
        messages.success(request, f'Course "{course_name}" added successfully!')

    return render(request, 'users/add_course.html')

@login_required
def add_workshop(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        date = request.POST.get('date')
        time = request.POST.get('time')
        duration = request.POST.get('duration')
        meetLink = request.POST.get('meetLink')
        instructor = request.POST.get('instructor')
        poster = request.FILES.get('poster')

        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            time_obj = datetime.strptime(time, "%H:%M").time()
            duration_float = float(duration)  # ← Accept 1.5 etc
            duration_obj = timedelta(hours=duration_float)
        except ValueError:
            messages.error(request, "Invalid date or duration format.")
            return render(request, 'users/add_workshop.html')

        # Here you would typically save the workshop to the database
        Workshop.objects.create(
            title=title,
            description=description,
            price=price,
            date=date_obj,
            time=time_obj,
            duration=duration_obj,
            meetLink=meetLink,
            instructor=instructor,
            poster=poster
        )
        messages.success(request, f'Workshop "{title}" added successfully!')

    return render(request, 'users/add_workshop.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_courses(request):
    courses = Course.objects.all()
    return render(request, 'users/manage_courses.html', {'courses': courses})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_workshops(request):
    workshops = Workshop.objects.all()
    return render(request, 'users/manage_workshops.html', {'workshops': workshops})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        instructor = request.POST.get('instructor')
        poster = request.FILES.get('poster')
        courseVideoLink = request.POST.get('courseVideoLink')
        pdf = request.FILES.get('pdf')
        if instructor:
            course.instructor = instructor
        if title:
            course.title = title
        if description:
            course.description = description
        if price:
            course.price = price
        if poster:
            course.poster = poster
        if courseVideoLink:
            course.courseVideoLink = courseVideoLink
        if pdf:
            course.pdf = pdf 

        course.save()
        messages.success(request, f'Course "{course.title}" updated successfully!')
        return redirect('manage_courses')
    return render(request, 'users/edit_course.html', {'course': course})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('manage_courses')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        instructor = request.POST.get('instructor')
        poster = request.FILES.get('poster')
        dateAndTime = request.POST.get('dateAndTime')
        duration = request.POST.get('duration')
        meetLink = request.POST.get('meetLink')
        if instructor:
            workshop.instructor = instructor
        if title:
            workshop.title = title
        if description:
            workshop.description = description
        if price:
            workshop.price = price
        if poster:
            workshop.poster = poster
        if dateAndTime:
            workshop.dateAndTime = dateAndTime
        if duration:
            workshop.duration = duration
        if meetLink:
            workshop.meetLink = meetLink

        workshop.save()
        messages.success(request, f'Workshop "{workshop.title}" updated successfully!')
        return redirect('manage_workshops')
    return render(request, 'users/edit_workshop.html', {'workshop': workshop})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    workshop.delete()
    messages.success(request, f'Workshop "{workshop.title}" deleted successfully!')
    return redirect('manage_workshops')

def workshop_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    is_registered = WorkshopRegistration.objects.filter(user=request.user, workshop=workshop).exists()
    testimonials = [
        {'text': 'A mind-blowing session! I had no idea AI was used in black hole simulations. Absolutely loved it!',
         'author': 'Aarav Menon, Astrophysics Student'},
        {'text': 'The instructor was phenomenal. She connected deep science with AI in such a simple way!',
         'author': 'Meera R., AI Research Intern'},
        {'text': 'I came for space, stayed for AI! Truly a cosmic combo. Can’t wait for the next workshop.',
         'author': 'Tanmay Kapoor, Tech Enthusiast'},
    ]

    return render(request, 'users/workshop.html', {
        'workshop': workshop,
        'testimonials': testimonials,
        'is_registered' : is_registered,
    })

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = CourseEnrollment.objects.filter(user=request.user, course=course).exists()
    testimonials = [
        {'text': 'A mind-blowing session! I had no idea AI was used in black hole simulations. Absolutely loved it!',
         'author': 'Aarav Menon, Astrophysics Student'},
        {'text': 'The instructor was phenomenal. She connected deep science with AI in such a simple way!',
         'author': 'Meera R., AI Research Intern'},
        {'text': 'I came for space, stayed for AI! Truly a cosmic combo. Can’t wait for the next workshop.',
         'author': 'Tanmay Kapoor, Tech Enthusiast'},
    ]

    return render(request, 'users/course.html', {
        'course': course,
        'testimonials': testimonials,
        'is_enrolled': is_enrolled,
    })
