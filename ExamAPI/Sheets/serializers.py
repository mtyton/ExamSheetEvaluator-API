from rest_framework import serializers
from django.contrib.auth.models import Group,User
from .models import ExamSheet, Question, Attempt, Solution, CorrectAnswer, PointForAnswer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'group', 'url']

    def get_group(self, obj):
        group = Group.objects.filter(name="teachers")
        users = User.objects.filter(groups__in=group)
        if obj in users:
            return "teacher"
        else:
            return "student"


class ExamSheetSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ExamSheetSerializer, self).__init__(*args, **kwargs)
        users = User.objects.filter(id = self.context['request'].user.id)
        self.fields['owner'].queryset = users

    questions = serializers.SerializerMethodField()

    class Meta:
        model = ExamSheet
        fields = '__all__'

    def get_questions(self, obj):
        queryset = Question.objects.filter(sheet=obj)
        questions = []
        for q in queryset:
            questions.append(q.text)
        return questions


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    correct_answers = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        exams = ExamSheet.objects.filter(owner=user)
        self.fields['sheet'].queryset = exams

    class Meta:
        model = Question
        fields = '__all__'

    def get_correct_answers(self, obj):
        queryset = CorrectAnswer.objects.filter(question=obj)
        answers = []
        for q in queryset:
            answers.append(q.ans_text)
        return answers


class CorrectAnswerSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CorrectAnswerSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        exams = ExamSheet.objects.filter(owner=user)
        questions = []
        for e in exams:
            new_questions = e.get_questions()
            questions += new_questions
        self.fields['question'].queryset = CorrectAnswer.objects.filter(question__in=questions)

    class Meta:
        model = CorrectAnswer
        fields = '__all__'


class AttemptSerializer(serializers.HyperlinkedModelSerializer):
    solutions = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(AttemptSerializer, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name="students")
        self.fields['examinee'].queryset = User.objects.filter(groups__in=groups)

    class Meta:
        model = Attempt
        fields = '__all__'

    def get_solutions(self, obj):
        queryset = Solution.objects.filter(attempt=obj)
        solutions = []
        for q in queryset:
            solutions.append(q.ans_text)
        return solutions


class SolutionSerializer(serializers.HyperlinkedModelSerializer):
    points = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(SolutionSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['attempt'].queryset = Attempt.objects.filter(examinee=user)

    class Meta:
        model = Solution
        fields = ['attempt', 'given_text', 'points']

    def get_points(self, obj):
        queryset = PointForAnswer.objects.filter(solution=obj)
        solutions = []
        for q in queryset:
            solutions.append(q.ans_text)
        return solutions


class PointForAnswerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PointForAnswer
        fields = '__all__'
