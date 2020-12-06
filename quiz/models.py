from PIL import Image
from django.db import models
from django.contrib.auth.models import User

class Questions(models.Model):
    uestion = models.TextField("Текст вопроса")
    option1 = models.CharField("Вариант 1", max_length=100)
    option2 = models.CharField("Вариант 2", max_length=100)
    option3 = models.CharField("Вариант 3", max_length=100)
    option4 = models.CharField("Вариант 4", max_length=100)
    answer = models.CharField("Правильный вариант", max_length=100,
                              help_text="Правильный вариант должен полностью повторять один из вариантов")

    def __str__(self):
        return self.uestion

    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"


class QuizzComplete(models.Model):
    score = models.SmallIntegerField("Очки")
    student = models.OneToOneField(User, verbose_name="Студент", on_delete=models.CASCADE, primary_key=True)
    date = models.DateTimeField("Дата прохождения", auto_now_add=True)
    complete = models.BooleanField("Прошёл тест?", default=False)

    def __str__(self):
        if self.complete is False:
            text = 'Не прошёл'
        else:
            text = 'Прошёл'

        return f"{self.student} - Очков: {self.score} - {text} "

    class Meta:
        verbose_name = "Завершенные тесты"
        verbose_name_plural = "Завершенные тесты"


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    image = models.ImageField("Изображение", default='profile_pics/default-avatar.png', upload_to='profile_pics')

    def __str__(self):
        return f'Профиль {self.user.username}'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"