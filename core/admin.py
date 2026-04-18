from django.contrib import admin
from django.utils.html import format_html, mark_safe
from core.models import (
    Course, BlogPost, Testimonial, GalleryImage,
    Application, AboutPage, ContactInfo, AdminProfile, SiteSettings
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'intake_period', 'fees', 'is_active', 'order')
    list_filter = ('is_active', 'intake_period', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'featured_image')
        }),
        ('Course Details', {
            'fields': ('duration', 'intake_period', 'fees')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'views', 'is_featured', 'published_date')
    list_filter = ('status', 'is_featured', 'published_date', 'created_at')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'featured_image', 'excerpt')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Publishing', {
            'fields': ('author', 'status', 'is_featured', 'published_date')
        }),
        ('Statistics', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('published_date', 'created_at', 'updated_at', 'views')
    date_hierarchy = 'published_date'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'get_rating_stars', 'is_active', 'order')
    list_filter = ('is_active', 'rating', 'created_at')
    search_fields = ('name', 'course')
    fields = ('name', 'course', 'message', 'photo', 'rating', 'is_active', 'order')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_rating_stars(self, obj):
        return format_html(
            '<span style="color: gold;">{"★" * obj.rating}</span>',
            obj.rating
        )
    get_rating_stars.short_description = 'Rating'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_preview', 'is_active', 'order')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    fields = ('title', 'image', 'category', 'description', 'is_active', 'order')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" />',
                obj.image.url
            )
        return 'No image'
    image_preview.short_description = 'Preview'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'course', 'status', 'created_at')
    list_filter = ('status', 'course', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'ip_address')
    fieldsets = (
        ('Applicant Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Application Details', {
            'fields': ('course', 'message', 'status')
        }),
        ('Meta Information', {
            'fields': ('ip_address', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'
    actions = ['mark_as_reviewed', 'mark_as_accepted', 'mark_as_rejected']
    
    def mark_as_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    mark_as_reviewed.short_description = 'Mark selected as Reviewed'
    
    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')
    mark_as_accepted.short_description = 'Mark selected as Accepted'
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_as_rejected.short_description = 'Mark selected as Rejected'


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Page Title', {
            'fields': ('title',)
        }),
        ('College Information', {
            'fields': ('history', 'mission', 'vision', 'values', 'campus_description', 'location', 'established_year')
        }),
        ('Leadership', {
            'fields': ('principal_name', 'principal_message', 'principal_image')
        }),
    )
    readonly_fields = ('updated_at',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Details', {
            'fields': ('phone_primary', 'phone_secondary', 'email', 'email_alternative')
        }),
        ('Address', {
            'fields': ('address', 'postal_code', 'city', 'country')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'linkedin', 'instagram', 'youtube')
        }),
        ('Maps', {
            'fields': ('latitude', 'longitude')
        }),
        ('Operating Hours', {
            'fields': ('opening_hours',)
        }),
    )
    readonly_fields = ('updated_at',)


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'last_login_ip', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'full_name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'last_login_ip')
    fields = ('user', 'full_name', 'phone', 'avatar', 'bio', 'last_login_ip', 'created_at', 'updated_at')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'logo_preview', 'updated_at')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" style="height:40px;"/>')
        return '(No logo)'
    logo_preview.short_description = 'Logo Preview'
