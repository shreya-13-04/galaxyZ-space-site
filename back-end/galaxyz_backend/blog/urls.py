from django.urls import path
from . import views

urlpatterns = [
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('manage_blogs/', views.manage_blogs, name='manage_blogs'),
    path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),  # Reusing add_blog view for editing
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
]
