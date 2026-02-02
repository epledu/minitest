import os

from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Question, Quiz, Result


def _extract_score(request, question):
    score_value = request.POST.get("score")
    if score_value is not None:
        try:
            return int(score_value)
        except ValueError:
            return 0

    choice_id = request.POST.get("choice")
    if not choice_id:
        return 0

    choice = get_object_or_404(Choice, id=choice_id, question=question)
    if isinstance(choice.score, dict):
        total = 0
        for value in choice.score.values():
            try:
                total += int(value)
            except (TypeError, ValueError):
                continue
        return total
    return 0


# 1. 테스트 목록 (홈 화면)
def quiz_list(request):
    quizzes = Quiz.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "quiz/quiz_list.html", {"quizzes": quizzes})


# 2. 테스트 시작 (인트로) - 점수 초기화
def quiz_intro(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug, is_active=True)
    request.session["total_score"] = 0
    request.session["user_answers"] = []
    return render(request, "quiz/quiz_intro.html", {"quiz": quiz})


# 3. 질문 페이지 - 점수 누적 로직
def quiz_question(request, quiz_slug, question_id):
    quiz = get_object_or_404(Quiz, slug=quiz_slug, is_active=True)
    questions = quiz.questions.all().order_by("order", "id")
    question = get_object_or_404(Question, id=question_id, quiz=quiz)

    if request.method == "POST":
        choice_type = request.POST.get("choice_type")
        user_answers = request.session.get("user_answers", [])
        if choice_type:
            user_answers.append(choice_type)
            request.session["user_answers"] = user_answers
        else:
            score = _extract_score(request, question)
            request.session["total_score"] = request.session.get("total_score", 0) + score

        next_question = questions.filter(order__gt=question.order).first()
        if next_question:
            return redirect("quiz:quiz_question", quiz_slug=quiz.slug, question_id=next_question.id)
        return redirect("quiz:quiz_result", quiz_slug=quiz.slug)

    return render(request, "quiz/quiz_question.html", {"quiz": quiz, "question": question})


# 4. 결과 페이지 - 타입/점수 혼합 매칭
def quiz_result(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug, is_active=True)
    user_answers = request.session.get("user_answers", [])

    type_scores = {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0}
    for i, ans_type in enumerate(user_answers):
        weight = 1.5 if i >= 6 else 1.0
        if ans_type in type_scores:
            type_scores[ans_type] += weight

    final_type = max(type_scores, key=type_scores.get) if user_answers else None

    if final_type:
        result = Result.objects.filter(quiz=quiz, result_type=final_type).first()
    else:
        score = request.session.get("total_score", 0)
        result = (
            Result.objects.filter(quiz=quiz, min_score__lte=score, max_score__gte=score)
            .order_by("min_score")
            .first()
        )

    context = {
        "quiz": quiz,
        "result": result,
        "score": request.session.get("total_score", 0),
        "kakao_js_key": os.getenv("KAKAO_JS_KEY"),
        "kakao_share_image_url": os.getenv("KAKAO_SHARE_IMAGE_URL"),
    }
    return render(request, "quiz/quiz_result.html", context)


def error_404(request, exception):
    return render(request, "404.html", status=404)
