import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quiz.models import Question, Choice, Result

def seed_data():
    print("데이터 주입 시작...")

    # 1. 결과 데이터 (필드명: title, key)
    results_data = [
        {'title': '테토남 (Teto-M)', 'key': 'Teto_M', 'description': '강한 주도성과 추진력의 알파메일!'},
        {'title': '테토녀 (Teto-W)', 'key': 'Teto_W', 'description': '당당한 매력의 걸크러쉬!'},
        {'title': '에겐남 (Egen-M)', 'key': 'Egen_M', 'description': '섬세하고 따뜻한 힐러!'},
        {'title': '에겐녀 (Egen-W)', 'key': 'Egen_W', 'description': '수용적인 감성의 소유자!'},
    ]

    for r in results_data:
        Result.objects.get_or_create(title=r['title'], key=r['key'], defaults={'description': r['description']})

    # 2. 질문 데이터
    questions_list = [
        {
            "text": "배달 음식이 1시간 넘게 안 올 때 나의 반응은?",
            "choices": [
                {"text": "바로 전화해서 따진다", "score": {"Teto": 2}},
                {"text": "럭키비키잖아! 더 배고플 때 먹어야지", "score": {"Egen": 2}}
            ]
        },
        # (여기에 나머지 18개 질문을 위와 같은 형식으로 추가하세요)
    ]

    for i, q_data in enumerate(questions_list):
        question, created = Question.objects.get_or_create(
            text=q_data['text'],
            defaults={'order': i + 1}
        )
        if created:
            for c_data in q_data['choices']:
                # Choice 모델의 점수 필드명을 확인하세요. (trait_score 또는 score_impact 등)
                Choice.objects.create(
                    question=question,
                    text=c_data['text'],
                    trait_score=c_data['score'] 
                )

    print("데이터 주입 성공!")

if __name__ == '__main__':
    seed_data()