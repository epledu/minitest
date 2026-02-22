from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Quiz


class StaticPageSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        # 메인 페이지(테스트 목록)
        return ["quiz:quiz_list"]

    def location(self, item):
        return reverse(item)


class QuizResultSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Quiz.objects.filter(is_active=True).order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("quiz:quiz_result", kwargs={"quiz_slug": obj.slug})
