from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import Group, User
from .models import ExamSheet, Question
from .models import Point, Solution, Grade
from .serializers import ExamSheetSerializer, QuestionSerializer, UserSerializer
from .serializers import SolutionSerializer, PointSerializer, GradeSerializer
from .permissions import IsOwnerOrReadOnly, IsSheetOwnerOrReadOnly, IsExamineeOrReadOnly, GradePermissions, PointPermissions
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
    permission_classes = [IsSheetOwnerOrReadOnly, ]


class SolutionView(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [IsExamineeOrReadOnly, ]


class PointView(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [PointPermissions]


class GradeView(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [GradePermissions, ]