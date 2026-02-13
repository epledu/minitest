from django.contrib import admin

from .models import BlogImage, BlogPost, Choice, Question, Quiz, Result


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    fields = ("image", "caption", "placement", "order")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "summary", "intro", "body_1", "body_2", "body_3", "conclusion")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "og_image_url", "is_published")}),
        ("본문", {"fields": ("intro", "body_1", "body_2", "body_3", "conclusion")}),
        ("추가 인사이트", {"fields": ("deep_dive", "deep_dive_extra")}),
    )
    inlines = [BlogImageInline]


admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Result)
