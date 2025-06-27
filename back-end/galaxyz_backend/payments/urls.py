from django.urls import path
from . import views

urlpatterns = [
    path('enroll_course/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('enroll_workshop/<int:workshop_id>/', views.enroll_workshop, name='enroll_workshop'),
    path('payment_success_course/<int:course_id>/', views.payment_success_course, name='payment_success_course'),
    path('payment_success_workshop/<int:workshop_id>/', views.payment_success_workshop, name='payment_success_workshop'),
    path('payment_failure_course/<int:course_id>/', views.payment_failure_course, name='payment_failure_course'),
    path('payment_failure_workshop/<int:workshop_id>/', views.payment_failure_workshop, name='payment_failure_workshop'),
]
