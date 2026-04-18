from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from core.models import (
    Course, BlogPost, Testimonial, GalleryImage, 
    Application, AboutPage, ContactInfo
)
from core.forms import ApplicationForm, ContactForm


# ==================== HOME & GENERAL PAGES ====================

def home(request):
    """Home page view with featured content"""
    courses = Course.objects.filter(is_active=True).order_by('order')[:3]
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
    blog_posts = BlogPost.objects.filter(status='published').order_by('-published_date')[:3]
    gallery_images = GalleryImage.objects.filter(is_active=True).order_by('order')[:6]
    
    context = {
        'courses': courses,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
        'gallery_images': gallery_images,
    }
    return render(request, 'website/index.html', context)


def about(request):
    """About page view"""
    try:
        about_page = AboutPage.objects.first()
    except AboutPage.DoesNotExist:
        about_page = None
    
    context = {
        'about': about_page,
    }
    return render(request, 'website/about.html', context)


# ==================== COURSES ====================

def courses_list(request):
    """List all courses with search"""
    courses = Course.objects.filter(is_active=True).order_by('order')
    search_query = request.GET.get('search', '')
    
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(courses, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'courses': page_obj.object_list,
        'search_query': search_query,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'website/courses.html', context)


def course_detail(request, pk):
    """Course detail view"""
    course = get_object_or_404(Course, pk=pk, is_active=True)
    related_courses = Course.objects.filter(is_active=True).exclude(pk=pk)[:3]
    
    context = {
        'course': course,
        'related_courses': related_courses,
    }
    return render(request, 'website/course_detail.html', context)


# ==================== BLOG ====================

def blog_list(request):
    """List all blog posts"""
    posts = BlogPost.objects.filter(status='published').order_by('-published_date')
    search_query = request.GET.get('search', '')
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    # Get featured post
    try:
        featured_post = BlogPost.objects.filter(status='published', is_featured=True).latest('published_date')
    except BlogPost.DoesNotExist:
        featured_post = None
    
    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'featured_post': featured_post,
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'search_query': search_query,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'website/blog.html', context)


def blog_detail(request, slug):
    """Blog post detail view"""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment views
    post.views += 1
    post.save(update_fields=['views'])
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        status='published'
    ).exclude(pk=post.pk).order_by('-published_date')[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'website/blog_detail.html', context)


# ==================== GALLERY ====================

def gallery(request):
    """Gallery view"""
    images = GalleryImage.objects.filter(is_active=True).order_by('order')
    category = request.GET.get('category', '')
    
    if category:
        images = images.filter(category=category)
    
    # Pagination
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    categories = GalleryImage.CATEGORY_CHOICES
    
    context = {
        'page_obj': page_obj,
        'images': page_obj.object_list,
        'categories': categories,
        'selected_category': category,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'website/gallery.html', context)


# ==================== TESTIMONIALS ====================

def testimonials(request):
    """Testimonials view"""
    testimonials_list = Testimonial.objects.filter(is_active=True).order_by('order')
    
    # Pagination
    paginator = Paginator(testimonials_list, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'testimonials': page_obj.object_list,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'website/testimonials.html', context)


# ==================== APPLICATION ====================

@require_http_methods(["GET", "POST"])
def apply(request):
    """Application form view"""
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.ip_address = get_client_ip(request)
            application.save()
            
            messages.success(request, 'Application submitted successfully! We will contact you soon.')
            return redirect('website:home')
    else:
        form = ApplicationForm()
    
    courses = Course.objects.filter(is_active=True)
    
    try:
        contact_info = ContactInfo.objects.first()
    except ContactInfo.DoesNotExist:
        contact_info = None
    
    context = {
        'form': form,
        'courses': courses,
        'contact_info': contact_info,
    }
    return render(request, 'website/apply.html', context)


# ==================== CONTACT ====================

@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Handle contact form submission
            messages.success(request, 'Thank you for contacting us. We will respond shortly.')
            return redirect('website:contact')
    else:
        form = ContactForm()
    
    try:
        contact_info = ContactInfo.objects.first()
    except ContactInfo.DoesNotExist:
        contact_info = None
    
    context = {
        'form': form,
        'contact_info': contact_info,
    }
    return render(request, 'website/contact.html', context)


# ==================== NEWSLETTER ====================

@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Newsletter subscription"""
    email = request.POST.get('email', '')
    
    if email:
        # Handle newsletter subscription
        messages.success(request, 'Successfully subscribed to our newsletter!')
    else:
        messages.error(request, 'Please enter a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', 'website:home'))


# ==================== UTILITY FUNCTIONS ====================

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ==================== ERROR HANDLERS ====================

def page_not_found(request, exception):
    """Custom 404 handler"""
    try:
        return render(request, 'errors/404.html', status=404)
    except Exception:
        # Fallback simple response if template missing
        from django.http import HttpResponse
        return HttpResponse('Page not found', status=404)


def server_error(request):
    """Custom 500 handler"""
    try:
        return render(request, 'errors/500.html', status=500)
    except Exception:
        from django.http import HttpResponse
        return HttpResponse('Server error', status=500)
