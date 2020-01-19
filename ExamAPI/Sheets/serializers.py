from rest_framework import serializers
from django.contrib.auth.models import Group,User
from .models import ExamSheet, Question, Solution,  Point, Grade


class UserSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    owned_exams = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'group','owned_exams', 'url']

    def get_group(self, obj):
        """
        Simply returns a groups name to which user belongs
        """
        group = Group.objects.filter(name="teachers")
        users = User.objects.filter(groups__in=group)
        if obj in users:
            return "teachers"
        else:
            return "students"

    def get_owned_exams(self, obj):
        """
        Get exams owned by teacher
        """
        exams = []
        queryset = ExamSheet.objects.filter(owner=obj)
        for q in queryset:
            exams.append(q.title)
        return exams


class ExamSheetSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        """
        Teacher can only add examsheet with himself as an owner
        """
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
        """
        Teacher can add questions only to exams he owns
        """
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        exams = ExamSheet.objects.filter(owner=user)
        self.fields['sheet'].queryset = exams

    class Meta:
        model = Question
        fields = '__all__'


# BIG PROBLEM WITH THIS FOREIGN KEYES
class SolutionSerializer(serializers.HyperlinkedModelSerializer):
    score = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        """
        Examinee have to be in students group
        """
        super(SolutionSerializer, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name="students")
        user = self.context['request'].user
        self.fields['examinee'].queryset = User.objects.filter(groups__in=groups, username=user.username)

    class Meta:
        model = Solution
        fields = ['date','examinee', 'to_question', 'given_text', 'url', 'score']
        read_only_fields = ['date']

    def get_score(self, obj):
        score = Point.objects.filter(answer=obj.id).first()
        if score:
            return score.points
        else:
            return 0


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = '__all__'

    def validate_points(self, data):
        """
        only can assign 0 or 1 point
        so if gives higher/lower we change it
        """
        if data> 1:
            data = 1
        elif data < 0:
            data=0
        return data


class GradeSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        """
        User have to be in students group
        """
        super(GradeSerializer, self).__init__(*args, **kwargs)
        groups = Group.objects.filter(name="students")
        self.fields['user'].queryset = User.objects.filter(groups__in=groups)

    class Meta:
        model = Grade
        fields = '__all__'
