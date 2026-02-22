from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "quiz"

urlpatterns = [
    # 홈: 전체 테스트 목록
    path("", views.quiz_list, name="quiz_list"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),

    # 특정 테스트의 흐름
    path("t/<slug:quiz_slug>/", views.quiz_intro, name="quiz_intro"),
    path("t/<slug:quiz_slug>/guide/", views.quiz_guide, name="quiz_guide"),
    path("t/<slug:quiz_slug>/q/<int:question_id>/", views.quiz_question, name="quiz_question"),
    path("t/<slug:quiz_slug>/result/", views.quiz_result, name="quiz_result"),

    # 수익화 및 신뢰성 페이지
    path("privacy/", TemplateView.as_view(template_name="privacy.html"), name="privacy"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("contact/", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path("terms/", TemplateView.as_view(template_name="terms.html"), name="terms"),
    path("ads.txt", TemplateView.as_view(template_name="ads.txt", content_type="text/plain")),
]
