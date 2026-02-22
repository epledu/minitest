"""URL configuration for config project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from quiz.sitemaps import QuizResultSitemap, StaticPageSitemap


sitemaps = {
    "static": StaticPageSitemap,
    "quiz_results": QuizResultSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'google94fdff691543b099.html',
        TemplateView.as_view(
            template_name="google94fdff691543b099.html",
            content_type="text/html",
        ),
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django_sitemap"),
    path('', include('quiz.urls')),
]

handler404 = 'quiz.views.error_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
