# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Blog
from django.contrib import messages
from django.shortcuts import redirect

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blog/blog_detail.html', {'blog': blog})

def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        content = request.POST.get('content')
        author = request.POST.get('author')
        
        # Create a new blog instance
        new_blog = Blog(title=title, content=content, author=author)
        new_blog.save()
        
        return render(request, 'blog/blog_detail.html', {'blog': new_blog})
    
    return render(request, 'blog/add_blog.html')

def manage_blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/manage_blogs.html', {'blogs': blogs})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        blog.title = request.POST.get('title', blog.title)
        blog.subtitle = request.POST.get('subtitle', blog.subtitle)
        blog.author = request.POST.get('author', blog.author)
        blog.content = request.POST.get('content', blog.content)
        blog.save()
        messages.success(request, "Blog updated successfully!")
        return redirect('manage_blogs')
    return render(request, 'blog/edit_blog.html', {'blog': blog})

@login_required
@user_passes_test(lambda u: u.is_superuser) 
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, "Blog deleted successfully!")
    return redirect('manage_blogs')
