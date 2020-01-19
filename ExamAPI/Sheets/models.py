from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class ExamSheet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_questions(self):
        questions = Question.objects.filter(sheet=self)
        return questions


class Question(models.Model):
    sheet = models.ForeignKey(ExamSheet, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=200)

    def __str__(self):
        return "Test " + str(self.sheet) + " - Question: " + str(self.text)

    def get_solutions(self):
        solutions = Solution.objects.filter(to_question=self)
        return solutions

    def get_solutions_for_student(self, examinee):
        """
        get all solutions for this question but only for one student
        """
        solutions = Solution.objects.filter(examinee=examinee, to_question=self)
        return solutions


class Solution(models.Model):
    examinee = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    to_question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    given_text = models.CharField(max_length=100)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return "Asnwer: "+ str(self.given_text) + " BY: " + str(self.examinee)

    def get_points(self):
        """
        get points for this question
        """
        points = Point.objects.filter(answer=self).first()
        return points


class Point(models.Model):
    answer = models.OneToOneField(Solution, on_delete=models.DO_NOTHING, unique=True)
    points = models.IntegerField()


class Grade(models.Model):
    sheet = models.ForeignKey(ExamSheet, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    mark = models.IntegerField()
