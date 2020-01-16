from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# teachers are going to be examsheets owner
class ExamUser(User):
    pass


class ExamSheet(models.Model):
    owner = models.ForeignKey(ExamUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

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
    ans_text = models.CharField(max_length=100)

    def __str__(self):
        return self.ans_text


class Attempt(models.Model):
    examinee = models.ForeignKey(ExamUser, on_delete=models.CASCADE)
    sheet = models.ForeignKey(ExamSheet, on_delete=models.CASCADE)

    def get_answers_per_attempt(self):
        answers = Solution.objects.filter(attempt=self)


class Solution(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    to_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    given_text = models.CharField(max_length=100)

    def check_accuracy(self):
        answers = self.to_question.get_answers()
        for ans in answers:
            if ans.ans_text == self.given_text:
                return True
        return False


class PointForAnswer(models.Model):
    answer = models.ForeignKey(Solution, on_delete=models.CASCADE)
    points = models.IntegerField()