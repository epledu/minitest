"""URL configuration for config project."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'google94fdff691543b099.html',
        TemplateView.as_view(
            template_name="google94fdff691543b099.html",
            content_type="text/html",
        ),
    ),
    path('', include('quiz.urls')),
]

handler404 = 'quiz.views.error_404'
