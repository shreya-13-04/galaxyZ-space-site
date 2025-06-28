from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_course/', views.add_course, name='add_course'),
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('add_workshop/', views.add_workshop, name='add_workshop'),
    path('manage_workshops/', views.manage_workshops, name='manage_workshops'),
    path('edit_workshop/<int:workshop_id>/', views.edit_workshop, name='edit_workshop'),
    path('workshop/<int:workshop_id>/delete/', views.delete_workshop, name='delete_workshop'),
    path('workshop/<int:workshop_id>/', views.workshop_detail, name='workshop_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('convert_workshop_to_course/<int:workshop_id>/', views.convert_workshop_to_course, name='convert_workshop_to_course'),
]
