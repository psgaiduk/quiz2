from django.contrib import admin
from .models import Questions, QuizzComplete, Profile

admin.site.register(Questions)
admin.site.register(QuizzComplete)
admin.site.register(Profile)