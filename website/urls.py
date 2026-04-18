from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Public website routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses_list, name='courses_list'),
    path('course/<int:pk>/', views.course_detail, name='courses_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('apply/', views.apply, name='apply'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
