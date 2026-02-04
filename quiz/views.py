import os

import random

from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Question, Quiz, Result

BLOG_POSTS = [
    {
        "slug": "dopamine-detox-guide",
        "title": "도파민 디톡스, 정말 필요한 사람은 누구일까?",
        "summary": "자극 피로가 쌓이는 신호와 회복 루틴을 정리합니다.",
        "content": [
            "짧고 강한 자극을 반복적으로 받으면 뇌는 더 강한 자극을 기대하게 됩니다. 이때 작은 일상의 만족이 잘 느껴지지 않는다면, 디지털 과식의 신호일 수 있어요.",
            "도파민 디톡스는 완전한 차단이 아니라, 자극의 강도를 낮추고 회복 가능한 리듬을 만드는 과정입니다. 하루 10분의 '노-스크롤' 시간을 확보하는 것만으로도 시작이 가능합니다.",
            "핵심은 '끊기'보다 '바꾸기'입니다. 자극을 줄이는 대신, 낮은 자극으로도 만족 가능한 활동(산책, 독서, 짧은 정리)을 루틴화해 보세요.",
        ],
    },
    {
        "slug": "micro-spending-patterns",
        "title": "마이크로 소비, 왜 작은 결제가 더 강할까?",
        "summary": "소확행 소비의 심리와 후회 포인트를 짚어봅니다.",
        "content": [
            "작은 결제는 심리적 마찰이 낮아 '보상'을 빠르게 제공합니다. 하지만 반복되면 누적 비용이 커지거나 만족감이 줄어드는 역효과가 생길 수 있어요.",
            "중요한 건 소비 자체가 아니라 소비 후의 감정입니다. '즐거움이 얼마나 지속되는지'를 기준으로 소비를 재정렬해 보세요.",
            "가장 쉬운 방법은 예산의 상한선을 정하는 것. 금액이 아니라 빈도만 줄여도 체감이 큽니다.",
        ],
    },
    {
        "slug": "loneliness-management",
        "title": "외로움은 없애는 게 아니라 관리하는 것",
        "summary": "혼자 있는 시간과 연결의 균형을 다룹니다.",
        "content": [
            "외로움은 누군가가 곁에 없어서가 아니라, 지금의 나와 연결이 끊겼을 때 더 크게 느껴집니다.",
            "혼놀 인프라를 만드는 사람도, 짧은 연결을 선호하는 사람도 모두 괜찮습니다. 중요한 건 나에게 맞는 회복 방식입니다.",
            "오늘은 아주 짧은 연결(안부 메시지 1개) 혹은 깊은 연결(30분 대화) 중 하나를 택해 보세요.",
        ],
    },
    {
        "slug": "intentional-life-vs-optimization",
        "title": "의도적 삶 vs 효율 과몰입, 내 균형점 찾기",
        "summary": "리추얼과 효율 사이에서 나만의 기준을 세웁니다.",
        "content": [
            "효율을 중시하는 삶은 성취감을 주지만, 너무 빠르면 현재를 놓치기 쉽습니다.",
            "반대로 리추얼 중심의 삶은 안정감을 주지만, 현실의 속도를 무시할 수는 없습니다.",
            "둘 사이의 균형은 '지금 나에게 필요한 것'을 기준으로 잡는 것이 가장 현실적입니다.",
        ],
    },
    {
        "slug": "liquid-content-consumption",
        "title": "숏폼에서 롱폼까지, 나만의 콘텐츠 소비 루트",
        "summary": "콘텐츠를 소비하고 남기는 방식이 곧 습관입니다.",
        "content": [
            "짧게 많이 보는 습관은 즉각적인 재미를 주지만, 기억에 남는 것은 적습니다.",
            "저장/정주행형은 몰입을 주지만, 실행까지 시간이 필요합니다.",
            "내가 어떤 방식으로 정보를 남기는지 알면, 더 효율적인 소비 루트를 설계할 수 있습니다.",
        ],
    },
    {
        "slug": "digital-burnout-signals",
        "title": "디지털 번아웃 신호 5가지",
        "summary": "피로가 누적되기 전 신호를 점검하세요.",
        "content": [
            "1) 쉬어도 피곤하다. 2) 자극이 없으면 무기력하다. 3) 집중이 잘 되지 않는다.",
            "4) 자꾸만 알림을 확인한다. 5) 콘텐츠를 소비해도 허무하다.",
            "이 중 2개 이상이라면, 자극 강도를 낮추는 루틴이 필요합니다.",
        ],
    },
    {
        "slug": "habit-reset",
        "title": "루틴이 무너졌을 때 다시 세우는 3단계",
        "summary": "작게 시작해 되살리는 루틴 회복법.",
        "content": [
            "첫째, 하루 1개 행동만 정합니다. 둘째, 시간보다 순서를 정합니다. 셋째, 기록보다 체감을 우선합니다.",
            "루틴은 크기가 아니라 반복이 핵심입니다. 작더라도 '매일'이 중요합니다.",
        ],
    },
    {
        "slug": "content-diet",
        "title": "콘텐츠 다이어트, 실패하지 않는 방법",
        "summary": "줄이기보다 교체하기에 집중합니다.",
        "content": [
            "나쁜 습관을 끊는 것보다 좋은 습관으로 바꾸는 것이 오래갑니다.",
            "콘텐츠 시간을 '대체 활동'으로 바꾸면 실패 확률이 크게 줄어듭니다.",
        ],
    },
    {
        "slug": "mini-mission-power",
        "title": "작은 미션이 큰 변화를 만드는 이유",
        "summary": "실행 가능한 미션이 결과를 현실로 바꿉니다.",
        "content": [
            "미션이 작을수록 실행 확률이 높습니다. 실행이 쌓이면 성향도 변합니다.",
            "결과를 '읽는 것'이 아니라 '하는 것'으로 바꾸는 게 핵심입니다.",
        ],
    },
    {
        "slug": "how-to-read-results",
        "title": "테스트 결과를 똑똑하게 읽는 법",
        "summary": "결과는 방향을 제시할 뿐, 정답이 아닙니다.",
        "content": [
            "결과는 현재의 경향을 보여주는 거울입니다. 고정된 정체성이 아니에요.",
            "핵심은 결과에서 제안하는 행동을 '나에게 맞게' 조정하는 것입니다.",
        ],
    },
]

QUIZ_GUIDES = {
    "dopamine-test": {
        "title": "도파민 디톡스 지수 테스트 해설",
        "summary": "자극 피로가 쌓일 때 나타나는 패턴과 회복 루틴을 정리합니다.",
        "sections": [
            {
                "heading": "이 테스트가 보는 것",
                "body": "짧고 강한 자극에 얼마나 자주 반응하는지, 그리고 그 이후의 회복 패턴을 확인합니다. ‘즐거움’이 줄어들고 ‘피로감’이 남는 순간이 많다면, 자극의 강도를 조절할 필요가 있습니다.",
            },
            {
                "heading": "결과를 해석하는 방법",
                "body": "결과는 ‘고정된 성격’이 아니라 지금의 리듬을 보여주는 스냅샷입니다. 상황에 따라 얼마든지 달라질 수 있으니, 오늘의 상태를 가볍게 참고해 주세요.",
            },
            {
                "heading": "실행 팁",
                "body": "하루 10분의 노-스크롤 시간, 한 번의 산책, 한 가지 정리부터 시작해 보세요. 큰 변화보다 작은 반복이 효과적입니다.",
            },
        ],
    },
    "micro-spending": {
        "title": "마이크로 소비 성향 테스트 해설",
        "summary": "작은 결제가 남기는 감정과 만족의 지속성을 살펴봅니다.",
        "sections": [
            {
                "heading": "이 테스트가 보는 것",
                "body": "소비 동기가 ‘기분 보상’인지, ‘효율 개선’인지, 혹은 ‘기억 수집’인지에 따라 일상이 달라집니다. 작은 결제는 습관이 되기 쉬워요.",
            },
            {
                "heading": "결과를 해석하는 방법",
                "body": "결과는 ‘잘/못’이 아니라 ‘나에게 맞는 소비 방식’을 알려주는 힌트입니다. 만족감이 오래 가는 소비를 기준으로 재정렬해 보세요.",
            },
            {
                "heading": "실행 팁",
                "body": "한 달 예산을 세분화하기보다, ‘주간 구매 빈도’를 줄이는 것만으로도 체감 변화가 큽니다.",
            },
        ],
    },
    "loneliness-management": {
        "title": "외로움 관리 스타일 테스트 해설",
        "summary": "혼자 있는 시간과 연결의 균형을 어떻게 맞추는지에 집중합니다.",
        "sections": [
            {
                "heading": "이 테스트가 보는 것",
                "body": "외로움은 연결의 양보다 ‘나에게 맞는 연결 방식’이 부족할 때 커집니다. 혼자만의 시간도, 가벼운 소셜도 모두 정답이 될 수 있어요.",
            },
            {
                "heading": "결과를 해석하는 방법",
                "body": "결과는 나의 회복 방식을 보여줍니다. 지금의 회복 방식이 유지 가능한지, 부담이 없는지 확인해 보세요.",
            },
            {
                "heading": "실행 팁",
                "body": "짧은 안부 메시지 1개 또는 깊은 대화 1번 중 하나만 선택해도 충분합니다.",
            },
        ],
    },
    "intentional-vs-optimization": {
        "title": "의도적 삶 vs 효율 과몰입 테스트 해설",
        "summary": "리추얼과 효율 사이에서 나의 균형점을 찾는 테스트입니다.",
        "sections": [
            {
                "heading": "이 테스트가 보는 것",
                "body": "성취 중심의 효율과, 삶의 감각을 되살리는 리추얼 사이에서 어디에 가까운지 확인합니다.",
            },
            {
                "heading": "결과를 해석하는 방법",
                "body": "균형은 정답이 아닙니다. 지금 내 삶에 필요한 것을 우선순위로 두는 것이 현실적인 해석입니다.",
            },
            {
                "heading": "실행 팁",
                "body": "하루에 단 하나의 ‘의식’을 만들거나, 반대로 효율을 높일 작은 자동화를 하나만 추가해 보세요.",
            },
        ],
    },
    "liquid-content": {
        "title": "콘텐츠 소비 스타일 테스트 해설",
        "summary": "짧게 많이 보는 흐름과 깊게 남기는 습관을 비교합니다.",
        "sections": [
            {
                "heading": "이 테스트가 보는 것",
                "body": "콘텐츠를 소비한 뒤 남는 것이 무엇인지에 집중합니다. ‘재미’, ‘기억’, ‘정리’ 중 무엇이 중심인지 확인해 보세요.",
            },
            {
                "heading": "결과를 해석하는 방법",
                "body": "결과는 소비 방식의 장단점을 보여줍니다. 부족한 부분을 하나만 보완하면 균형이 잡힙니다.",
            },
            {
                "heading": "실행 팁",
                "body": "하루 한 번은 ‘정리/저장/공유’ 중 하나를 의도적으로 해보세요. 소비의 질이 달라집니다.",
            },
        ],
    },
}


def blog_list(request):
    return render(request, "blog/blog_list.html", {"posts": BLOG_POSTS, "show_ads": True})


def blog_detail(request, slug):
    post = next((p for p in BLOG_POSTS if p["slug"] == slug), None)
    if not post:
        return render(request, "404.html", status=404)
    return render(request, "blog/blog_detail.html", {"post": post, "show_ads": True})


def quiz_guide(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug, is_active=True)
    guide = QUIZ_GUIDES.get(quiz.slug)
    return render(
        request,
        "quiz/quiz_guide.html",
        {"quiz": quiz, "guide": guide, "show_ads": True},
    )


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
    return render(request, "quiz/quiz_list.html", {"quizzes": quizzes, "show_ads": True})


# 2. 테스트 시작 (인트로) - 점수 초기화
def quiz_intro(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug, is_active=True)
    request.session["total_score"] = 0
    request.session["user_answers"] = []
    return render(request, "quiz/quiz_intro.html", {"quiz": quiz, "show_ads": False})


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

    return render(
        request,
        "quiz/quiz_question.html",
        {"quiz": quiz, "question": question, "show_ads": False},
    )


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

    rarity = random.randint(3, 12)
    base_type = final_type or getattr(result, "result_type", None)
    match_result = None
    if base_type:
        other_types = [t for t in ["A", "B", "C", "D"] if t != base_type]
        if other_types:
            match_type = random.choice(other_types)
            match_result = Result.objects.filter(quiz=quiz, result_type=match_type).first()

    context = {
        "quiz": quiz,
        "result": result,
        "score": request.session.get("total_score", 0),
        "kakao_js_key": os.getenv("KAKAO_JS_KEY"),
        "kakao_share_image_url": os.getenv("KAKAO_SHARE_IMAGE_URL"),
        "rarity": rarity,
        "match_result": match_result,
        "show_ads": True,
    }
    return render(request, "quiz/quiz_result.html", context)


def error_404(request, exception):
    return render(request, "404.html", status=404)
