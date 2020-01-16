from django.contrib import admin
from .models import ExamUser, ExamSheet, CorrectAnswer, Question

# Register your models here.
admin.site.register(ExamUser)
admin.site.register(ExamSheet)
admin.site.register(CorrectAnswer)
admin.site.register(Question)
