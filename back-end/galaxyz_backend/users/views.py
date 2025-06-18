from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def dashboard(request):
    return render(request, 'users/dashboard.html')
# Render register page and handle POST request
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    users = User.objects.all()
    return render(request, 'users/admin_panel.html', {'users': users})