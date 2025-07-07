from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import Course, Workshop, CourseEnrollment, WorkshopRegistration
from django.shortcuts import get_object_or_404
from datetime import timedelta,datetime
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@login_required
def payment_success_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # Check again if already enrolled (safety)
        if not CourseEnrollment.objects.filter(user=user, course=course).exists():
            CourseEnrollment.objects.create(user=user, course=course)
            course.numberOfRegisteredUsers += 1
            course.save()
        
        is_enrolled = CourseEnrollment.objects.filter(user=request.user, course=course).exists()
        testimonials = [
        {'text': 'A mind-blowing session! I had no idea AI was used in black hole simulations. Absolutely loved it!',
         'author': 'Aarav Menon, Astrophysics Student'},
        {'text': 'The instructor was phenomenal. She connected deep science with AI in such a simple way!',
         'author': 'Meera R., AI Research Intern'},
        {'text': 'I came for space, stayed for AI! Truly a cosmic combo. Can’t wait for the next workshop.',
         'author': 'Tanmay Kapoor, Tech Enthusiast'},
        ]

        messages.success(request, f'Payment successful! You are now enrolled in "{course.title}"')
        return render(request, 'users/course.html', {
        'course': course,
        'testimonials': testimonials,
        'is_enrolled': is_enrolled,
    })

@csrf_exempt
@login_required
def payment_success_workshop(request, workshop_id):
    if request.method == 'POST':
        workshop = get_object_or_404(Workshop, id=workshop_id)
        user = request.user

        # Check again if already enrolled (safety)
        if not WorkshopRegistration.objects.filter(user=user, workshop=workshop).exists():
            CourseEnrollment.objects.create(user=user, workshop=workshop)
            workshop.numberOfRegisteredUsers += 1
            workshop.save()
        
        is_registered = WorkshopRegistration.objects.filter(user=request.user, workshop=workshop).exists()
        testimonials = [
        {'text': 'A mind-blowing session! I had no idea AI was used in black hole simulations. Absolutely loved it!',
         'author': 'Aarav Menon, Astrophysics Student'},
        {'text': 'The instructor was phenomenal. She connected deep science with AI in such a simple way!',
         'author': 'Meera R., AI Research Intern'},
        {'text': 'I came for space, stayed for AI! Truly a cosmic combo. Can’t wait for the next workshop.',
         'author': 'Tanmay Kapoor, Tech Enthusiast'},
        ]

        messages.success(request, f'Payment successful! You are now enrolled in "{workshop.title}"')
        return render(request, 'users/workshop.html', {
        'workshop': workshop,
        'testimonials': testimonials,
        'is_registered' : is_registered,
    })
    
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if CourseEnrollment.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
        return redirect('course_detail', course_id=course.id)

    # Create Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create order
    amount_paise = int(course.price * 100)  # convert to paise
    payment = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': 1
    })

    context = {
        'course': course,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    }
    return render(request, 'payments/checkout.html', context)

@login_required
def enroll_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)

    if WorkshopRegistration.objects.filter(user=request.user, workshop=workshop).exists():
        messages.warning(request, 'You are already registered for this workshop.')
        return redirect('workshop_detail', workshop_id=workshop.id)
    # Create Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    # Create order
    amount_paise = int(workshop.price * 100)  # convert to paise
    payment = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': 1
    })
    context = {
        'workshop': workshop,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    }
    return render(request, 'payments/checkout_workshop.html', context)


def payment_failure_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reason = request.GET.get('reason', 'Unknown error occurred.')
    return render(request, 'payments/failure.html', {'course': course, 'reason': reason})

def payment_failure_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    reason = request.GET.get('reason', 'Unknown error occurred.')
    return render(request, 'payments/failure_workshop.html', {'workshop': workshop, 'reason': reason})