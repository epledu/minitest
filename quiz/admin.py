from django.contrib import admin

from .models import BlogPost, Choice, Question, Quiz, Result


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "og_image_url", "is_published")}),
        ("본문", {"fields": ("intro", "body_1", "body_2", "body_3", "conclusion")}),
        ("추가 인사이트", {"fields": ("deep_dive", "deep_dive_extra")}),
    )


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Result)
