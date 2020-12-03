from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Quizz(models.Model):
    quiz = models.CharField(max_length=100)

class Questions(models.Model):
    quiz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

class QuizzComplete(models.Model):
    quiz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    student = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
