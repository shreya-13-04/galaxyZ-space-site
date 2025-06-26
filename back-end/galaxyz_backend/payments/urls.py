from django.urls import path
from . import views

urlpatterns = [
    path('enroll_course/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('payment_success/', views.payment_success, name='payment_success'),
]
