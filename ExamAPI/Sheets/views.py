from django.shortcuts import render
from rest_framework import viewsets
from .models import ExamSheet, Teacher, Question, CorrectAnswer, Student
from .models import PointForAnswer, Attempt, Solution
from .serializers import ExamSheetSerializer, TeacherSerializer, QuestionSerializer, CorrectAnswerSerializer, StudentSerializer
from .serializers import AttemptSerializer, SolutionSerializer, PointForAnswerSerializer


class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


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