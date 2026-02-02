from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="quiz_thumbs/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", default=1)
    text = models.CharField(max_length=500)
    choice_a = models.CharField(max_length=200, default="")
    choice_b = models.CharField(max_length=200, default="")
    choice_c = models.CharField(max_length=200, default="")
    choice_d = models.CharField(max_length=200, default="")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"[{self.quiz.title}] {self.text}"


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    score = models.JSONField(default=dict, help_text="e.g. {'Teto': 2}")

    def __str__(self):
        return self.text


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results", default=1)
    title = models.CharField(max_length=200)
    result_type = models.CharField(max_length=1, blank=True)
    one_liner = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    mission = models.CharField(max_length=255, blank=True)
    share_image_url = models.URLField(blank=True)
    min_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return f"[{self.quiz.title}] {self.title}"
