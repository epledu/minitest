import os

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Choice, Question, Result
from .services.scoring import (
    AFFILIATE_RECS,
    DEFAULT_AFFILIATE,
    SessionScoreService,
    get_share_image_url,
    pick_best_trait,
)


def _ordered_questions():
    return list(Question.objects.order_by("order", "id").prefetch_related("choices"))


def index(request):
    first_question = Question.objects.order_by("order", "id").first()
    return render(request, "index.html", {"first_question": first_question})


def question(request, pk):
    questions = _ordered_questions()
    if not questions:
        return render(request, "question.html", {"question": None})

    index_map = {question.id: idx for idx, question in enumerate(questions)}
    if pk not in index_map:
        return redirect("quiz:question", pk=questions[0].id)

    current_index = index_map[pk]
    current_question = questions[current_index]
    error_message = None
    scorer = SessionScoreService(request.session)

    if request.method == "POST":
        choice_id = request.POST.get("choice")
        if not choice_id:
            error_message = "선택지를 골라주세요."
        else:
            choice = get_object_or_404(Choice, id=choice_id, question=current_question)
            scorer.add_scores(choice.score)

            next_index = current_index + 1
            if next_index < len(questions):
                return redirect("quiz:question", pk=questions[next_index].id)
            return redirect("quiz:loading")

    total = len(questions)
    progress = int((current_index + 1) / total * 100)

    context = {
        "question": current_question,
        "current": current_index + 1,
        "total": total,
        "progress": progress,
        "error_message": error_message,
    }
    return render(request, "question.html", context)


def loading(request):
    scorer = SessionScoreService(request.session)
    if not scorer.get_scores():
        return redirect("quiz:index")
    return render(request, "loading.html", {"result_url": reverse("quiz:result")})


def result(request):
    scorer = SessionScoreService(request.session)
    scores = scorer.get_scores()
    if not scores:
        return redirect("quiz:index")

    best_key = pick_best_trait(scores)
    if not best_key:
        return redirect("quiz:index")

    result_item = Result.objects.filter(key=best_key).only("key", "title", "description").first()
    if not result_item:
        result_item = Result(
            key=best_key,
            title=best_key,
            description="결과 데이터를 준비 중입니다.",
        )

    share_url = request.build_absolute_uri(reverse("quiz:result"))
    retake_url = request.build_absolute_uri(reverse("quiz:restart"))
    kakao_js_key = os.getenv("KAKAO_JS_KEY") or getattr(settings, "KAKAO_JS_KEY", "")
    share_image_url = get_share_image_url(
        request,
        best_key,
        getattr(settings, "KAKAO_SHARE_IMAGE_URL", ""),
    )
    affiliate_links = AFFILIATE_RECS.get(best_key, DEFAULT_AFFILIATE)

    context = {
        "result": result_item,
        "result_key": best_key,
        "trait_key": best_key,
        "share_url": share_url,
        "retake_url": retake_url,
        "kakao_js_key": kakao_js_key,
        "share_image_url": share_image_url,
        "kakao_share_image_url": os.getenv("KAKAO_SHARE_IMAGE_URL") or share_image_url,
        "affiliate_links": affiliate_links,
    }
    return render(request, "result.html", context)


def restart(request):
    request.session.flush()
    return redirect("quiz:index")


def error_404(request, exception):
    return render(request, "404.html", status=404)
