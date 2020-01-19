from django.shortcuts import render
from rest_framework import viewsets, filters
from django.contrib.auth.models import Group, User
from .models import ExamSheet, Question
from .models import Point, Solution, Grade
from .serializers import ExamSheetSerializer, QuestionSerializer, UserSerializer
from .serializers import SolutionSerializer, PointSerializer, GradeSerializer
from .permissions import ExamSheetPermission, QuestionPermission, IsExamineeOrReadOnly, GradePermissions, PointPermissions
from rest_framework.permissions import IsAuthenticated


class UserView(viewsets.ReadOnlyModelViewSet):
    groups = Group.objects.filter(name__in=["teachers", "students"])
    queryset = User.objects.filter(groups__in=groups)
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['username']
    search_fields = ['username']


class ExamSheetView(viewsets.ModelViewSet):
    queryset = ExamSheet.objects.all()
    serializer_class = ExamSheetSerializer
    permission_classes = [ExamSheetPermission, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['title']
    search_fields = ['title']


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [QuestionPermission, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['text']
    search_fields = ['text']


class SolutionView(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [IsExamineeOrReadOnly, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['given_text']
    search_fields = ['given_text']


class PointView(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [PointPermissions]


class GradeView(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [GradePermissions, ]