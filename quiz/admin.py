from django.contrib import admin
from .models import Questions, Quizz, QuizzComplete

admin.site.register(Questions)
admin.site.register(Quizz)
admin.site.register(QuizzComplete)