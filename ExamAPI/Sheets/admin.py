from django.contrib import admin
from .models import ExamSheet, Question, Solution, Point, Grade

# Register your models here.
admin.site.register(ExamSheet)
admin.site.register(Question)
admin.site.register(Solution)
admin.site.register(Point)
admin.site.register(Grade)
