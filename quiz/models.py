from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    score = models.JSONField(default=dict, help_text="e.g. {'Teto': 2}")

    def __str__(self):
        return self.text


class Result(models.Model):
    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
