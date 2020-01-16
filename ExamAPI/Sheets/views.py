from django.shortcuts import render
from rest_framework import viewsets
from .models import ExamSheet, Question, CorrectAnswer
from .models import PointForAnswer, Attempt, Solution, ExamUser
from .serializers import ExamSheetSerializer, QuestionSerializer, CorrectAnswerSerializer, ExamUserSerializer
from .serializers import AttemptSerializer, SolutionSerializer, PointForAnswerSerializer


class ExamUserView(viewsets.ModelViewSet):
    queryset = ExamUser.objects.all()
    serializer_class = ExamUserSerializer


class ExamSheetView(viewsets.ModelViewSet):
    queryset = ExamSheet.objects.all()
    serializer_class = ExamSheetSerializer


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CorrectAnswerView(viewsets.ModelViewSet):
    queryset = CorrectAnswer.objects.all()
    serializer_class = CorrectAnswerSerializer


class AttemptView(viewsets.ModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer


class SolutionView(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class PointView(viewsets.ModelViewSet):
    queryset = PointForAnswer.objects.all()
    serializer_class = PointForAnswerSerializer