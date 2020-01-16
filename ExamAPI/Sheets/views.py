from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import Group
from .models import ExamSheet, Question, CorrectAnswer, User
from .models import PointForAnswer, Attempt, Solution
from .serializers import ExamSheetSerializer, QuestionSerializer, CorrectAnswerSerializer, UserSerializer
from .serializers import AttemptSerializer, SolutionSerializer, PointForAnswerSerializer


class UserView(viewsets.ReadOnlyModelViewSet):
    groups = Group.objects.filter(name__in=["teachers", "students"])
    queryset = User.objects.filter(groups__in=groups)
    serializer_class = UserSerializer


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