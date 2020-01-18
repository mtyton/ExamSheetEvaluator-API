from rest_framework import serializers
from django.contrib.auth.models import Group,User
from .models import ExamSheet, Question, Solution,  Point, Grade


class UserSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'group', 'url']

    def get_group(self, obj):
        """
        Simply returns a groups name to which user belongs
        """
        group = Group.objects.filter(name="teachers")
        users = User.objects.filter(groups__in=group)
        if obj in users:
            return "teacher"
        else:
            return "student"


class ExamSheetSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ExamSheetSerializer, self).__init__(*args, **kwargs)
        users = User.objects.filter(id=self.context['request'].user.id)
        self.fields['owner'].queryset = users

    questions = serializers.SerializerMethodField()

    class Meta:
        model = ExamSheet
        fields = '__all__'

    def get_questions(self, obj):
        """
        Simply returns all questions which belongs to this examsheet
        """
        queryset = Question.objects.filter(sheet=obj)
        questions = []
        for q in queryset:
            questions.append(q.text)
        return questions


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        exams = ExamSheet.objects.filter(owner=user)
        self.fields['sheet'].queryset = exams

    class Meta:
        model = Question
        fields = '__all__'


# BIG PROBLEM WITH THIS FOREIGN KEYES
class SolutionSerializer(serializers.HyperlinkedModelSerializer):

    def __init__(self, *args, **kwargs):
        super(SolutionSerializer, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name="students")
        self.fields['examinee'].queryset = User.objects.filter(groups__in=groups)

    class Meta:
        model = Solution
        fields = ['examinee', 'to_question', 'given_text']


class PointSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Point
        fields = '__all__'

    def validate_points(self, data):
        if data> 1:
            data = 1
        elif data < 0:
            data=0
        return data


class GradeSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(GradeSerializer, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name="students")
        self.fields['user'].queryset = User.objects.filter(groups__in=groups)

    class Meta:
        model = Grade
        fields = '__all__'