from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('website.urls', 'website'), namespace='website')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
     path(
        "sitemap.xml",
        TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml"),
        name="sitemap",
    ),
]
