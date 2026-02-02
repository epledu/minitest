"""URL configuration for config project."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    path(
        'ads.txt',
        TemplateView.as_view(template_name="ads.txt", content_type="text/plain"),
    ),
]

handler404 = 'quiz.views.error_404'
