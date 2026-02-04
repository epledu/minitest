from django.core.management.base import BaseCommand

from quiz.models import BlogPost
from quiz.views import BLOG_POSTS


class Command(BaseCommand):
    help = "Seed blog posts from in-code BLOG_POSTS list."

    def handle(self, *args, **options):
        created = 0
        updated = 0
        og_image_map = {
            "dopamine-detox-guide": "img/kakao_share.png",
            "micro-spending-patterns": "img/micro_kakao.png",
            "loneliness-management": "img/lonely_kakao.png",
            "intentional-life-vs-optimization": "img/liquid_main.png",
            "liquid-content-consumption": "img/content_main.png",
        }

        for post in BLOG_POSTS:
            sections = post.get("sections", [])
            intro = sections[0]["body"] if len(sections) > 0 else ""
            body_1 = sections[1]["body"] if len(sections) > 1 else ""
            body_2 = sections[2]["body"] if len(sections) > 2 else ""
            body_3 = sections[3]["body"] if len(sections) > 3 else ""
            conclusion = sections[4]["body"] if len(sections) > 4 else ""

            obj, is_created = BlogPost.objects.update_or_create(
                slug=post["slug"],
                defaults={
                    "title": post["title"],
                    "summary": post.get("summary", ""),
                    "og_image_url": og_image_map.get(post["slug"], ""),
                    "intro": intro,
                    "body_1": body_1,
                    "body_2": body_2,
                    "body_3": body_3,
                    "conclusion": conclusion,
                    "deep_dive": post.get("deep_dive", ""),
                    "deep_dive_extra": post.get("deep_dive_extra", ""),
                    "is_published": True,
                },
            )
            if is_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete: {created} created, {updated} updated."))
