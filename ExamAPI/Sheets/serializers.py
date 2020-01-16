from rest_framework import serializers
from .models import ExamSheet, Question, Attempt, Solution, CorrectAnswer, Teacher, Student, PointForAnswer


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    owned_exams = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['url','username', 'password', 'owned_exams']

    def get_owned_exams(self, obj):
        queryset = ExamSheet.objects.filter(owner=obj)
        exams = []
        for q in queryset:
            exams.append(q.title)
        return exams


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    attempts = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['url', 'username', 'password', 'attempts']

    def get_attempts(self, obj):
        queryset = Attempt.objects.filter(examinee=obj)
        attempts = []
        for q in queryset:
            attempts.append(q.url)
        return attempts


class ExamSheetSerializer(serializers.HyperlinkedModelSerializer):
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
    class Meta:
        model = CorrectAnswer
        fields = '__all__'


class AttemptSerializer(serializers.HyperlinkedModelSerializer):
    solutions = serializers.SerializerMethodField()

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

    class Meta:
        model = Attempt
        fields = '__all__'

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
