from django.shortcuts import render
from users.models import Workshop

def home(request):
    workshops = Workshop.objects.all().order_by('-date')
    return render(request, 'main/index.html', {'workshops': workshops})

