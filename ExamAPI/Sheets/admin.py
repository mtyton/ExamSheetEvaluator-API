from django.contrib import admin
from .models import Teacher, Student, ExamSheet, CorrectAnswer, Question

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(ExamSheet)
admin.site.register(CorrectAnswer)
admin.site.register(Question)
