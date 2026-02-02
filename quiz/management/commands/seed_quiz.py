from django.core.management.base import BaseCommand

from quiz.models import Choice, Question, Result


class Command(BaseCommand):
    help = "Seed sample quiz data for the Teto-Egen personality test."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing quiz data before seeding.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            Choice.objects.all().delete()
            Question.objects.all().delete()
            Result.objects.all().delete()

        results = [
            {
                "key": "테토남",
                "title": "테토남",
                "description": "강한 추진력과 직진형 리더십이 두드러지는 타입입니다.",
            },
            {
                "key": "테토녀",
                "title": "테토녀",
                "description": "자기주도적이며 주변을 이끄는 에너지가 강한 타입입니다.",
            },
            {
                "key": "에겐남",
                "title": "에겐남",
                "description": "섬세한 통찰과 배려로 관계를 깊게 만드는 타입입니다.",
            },
            {
                "key": "에겐녀",
                "title": "에겐녀",
                "description": "공감 능력이 높고 감정의 흐름을 잘 읽는 타입입니다.",
            },
        ]

        for data in results:
            Result.objects.update_or_create(
                key=data["key"],
                defaults={"title": data["title"], "description": data["description"]},
            )

        questions = [
            {
                "order": 1,
                "text": "새로운 프로젝트가 시작되면 나는?",
                "choices": [
                    ("빠르게 방향을 정하고 모두를 이끈다", {"테토남": 2}),
                    ("강하게 밀어붙이며 목표를 만든다", {"테토녀": 2}),
                    ("팀의 분위기와 관계를 먼저 살핀다", {"에겐남": 2}),
                    ("공감과 조율로 흐름을 정리한다", {"에겐녀": 2}),
                ],
            },
            {
                "order": 2,
                "text": "갈등이 생겼을 때 나는?",
                "choices": [
                    ("핵심만 짚고 결론을 빠르게 낸다", {"테토남": 2}),
                    ("단호하게 기준을 세우고 해결한다", {"테토녀": 2}),
                    ("상대의 감정을 먼저 이해한다", {"에겐남": 2}),
                    ("대화를 통해 부드럽게 풀어간다", {"에겐녀": 2}),
                ],
            },
            {
                "order": 3,
                "text": "내가 선호하는 리더십 스타일은?",
                "choices": [
                    ("전략을 짜고 전면에서 돌파", {"테토남": 2}),
                    ("목표를 공유하고 빠르게 실행", {"테토녀": 2}),
                    ("조용히 조율하며 팀을 받쳐준다", {"에겐남": 2}),
                    ("함께 공감하며 속도를 맞춘다", {"에겐녀": 2}),
                ],
            },
            {
                "order": 4,
                "text": "일상에서 에너지를 얻는 방식은?",
                "choices": [
                    ("도전적인 활동과 성취", {"테토남": 2}),
                    ("활동적이고 주도적인 일정", {"테토녀": 2}),
                    ("깊은 대화와 몰입", {"에겐남": 2}),
                    ("편안한 관계와 감정 교류", {"에겐녀": 2}),
                ],
            },
            {
                "order": 5,
                "text": "내가 더 중요하게 여기는 것은?",
                "choices": [
                    ("성과와 결과", {"테토남": 2}),
                    ("주도권과 임팩트", {"테토녀": 2}),
                    ("관계의 깊이", {"에겐남": 2}),
                    ("서로의 감정", {"에겐녀": 2}),
                ],
            },
        ]

        for data in questions:
            question, _ = Question.objects.update_or_create(
                text=data["text"],
                defaults={"order": data["order"]},
            )
            question.choices.all().delete()
            for choice_text, score in data["choices"]:
                Choice.objects.create(question=question, text=choice_text, score=score)

        self.stdout.write(self.style.SUCCESS("Sample quiz data created."))
