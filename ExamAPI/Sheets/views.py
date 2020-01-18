from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import Group, User
from .models import ExamSheet, Question, CorrectAnswer
from .models import PointForAnswer, Attempt, Solution
from .serializers import ExamSheetSerializer, QuestionSerializer, CorrectAnswerSerializer, UserSerializer
from .serializers import AttemptSerializer, SolutionSerializer, PointForAnswerSerializer
from .permissions import IsOwnerOrReadOnly, IsTeacher
from rest_framework.permissions import IsAuthenticated


class UserView(viewsets.ReadOnlyModelViewSet):
    groups = Group.objects.filter(name__in=["teachers", "students"])
    queryset = User.objects.filter(groups__in=groups)
    serializer_class = UserSerializer


class ExamSheetView(viewsets.ModelViewSet):
    queryset = ExamSheet.objects.all()
    serializer_class = ExamSheetSerializer
    permission_classes = [IsOwnerOrReadOnly, ]


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CorrectAnswerView(viewsets.ModelViewSet):
    queryset = CorrectAnswer.objects.all()
    serializer_class = CorrectAnswerSerializer
    permission_classes = [IsTeacher, IsAuthenticated]


class AttemptView(viewsets.ModelViewSet):
    queryset = Attempt.objects.all()
    serializer_class = AttemptSerializer


class SolutionView(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer


class PointView(viewsets.ModelViewSet):
    queryset = PointForAnswer.objects.all()
    serializer_class = PointForAnswerSerializer