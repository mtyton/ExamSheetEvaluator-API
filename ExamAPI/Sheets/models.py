from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# teachers are going to be examsheets owner
class Teacher(User):
    pass

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def get_teacher_exams(self):
        exams = ExamSheet.objects.filter(owner=self)
        return exams


class Student(User):

    class Meta:
        verbose_name = "Studnet"
        verbose_name_plural = "Students"

    def get_students_atempts(self):
        attempts = Attempt.objects.filter(examinee=Student)
        return attempts


class ExamSheet(models.Model):
    owner = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    length = models.IntegerField()  # TODO max length of a quiz

    def __str__(self):
        return self.title

    def get_questions(self):
        questions = Question.objects.filter(sheet=self)
        return questions


class Question(models.Model):
    sheet = models.ForeignKey(ExamSheet, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    def get_answers(self):
        return CorrectAnswer.objects.filter(question=self)


class CorrectAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans_text = models.CharField(max_length=200)

    def __str__(self):
        return self.ans_text


class Attempt(models.Model):
    examinee = models.ForeignKey(Student, on_delete=models.CASCADE)
    sheet = models.ForeignKey(ExamSheet, on_delete=models.CASCADE)


class GivenAnswer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    to_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    given_text = models.CharField(max_length=100)

    def check_accuracy(self):
        answers = self.to_question.get_answers()
        for ans in answers:
            if ans == self.given_text:
                return True
        return False


class PointForAnswer(models.Model):
    answer = models.ForeignKey(GivenAnswer, on_delete=models.CASCADE)
    points = models.IntegerField()