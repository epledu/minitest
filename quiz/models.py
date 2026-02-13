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
    mission_label = models.CharField(max_length=100, default="오늘의 추천 미션")
    one_liner = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    mission = models.TextField(blank=True)
    share_image_url = models.URLField(blank=True)
    min_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return f"[{self.quiz.title}] {self.title}"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    og_image_url = models.URLField(blank=True)
    intro = models.TextField()
    body_1 = models.TextField()
    body_2 = models.TextField()
    body_3 = models.TextField()
    conclusion = models.TextField()
    deep_dive = models.TextField(blank=True)
    deep_dive_extra = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BlogImage(models.Model):
    PLACEMENT_CHOICES = [
        ("header", "헤더"),
        ("intro", "서론"),
        ("body1", "본론 1"),
        ("body2", "본론 2"),
        ("body3", "본론 3"),
        ("conclusion", "결론"),
        ("deep_dive", "추가 인사이트"),
    ]

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="blog_images/")
    caption = models.CharField(max_length=200, blank=True)
    placement = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, default="body1")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["placement", "order", "id"]

    def __str__(self):
        return f"{self.post.title} - {self.get_placement_display()}"
