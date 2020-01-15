from rest_framework import serializers
from .models import ExamSheet, Question, Attempt, GivenAnswer, CorrectAnswer, Teacher, Student


class ExamSheetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ExamSheet
        fields = ['']