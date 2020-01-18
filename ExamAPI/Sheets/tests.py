from django.test import TestCase
from django.contrib.auth.models import Group, User
from .models import ExamSheet, Question, CorrectAnswer, Attempt, Solution, PointForAnswer
from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse
from .views import UserView, ExamSheetView


class TestExamSheetModel(TestCase):
    def setUp(self):
        self.teacher = User(username="test_teacher", password="testzaq1@WSX")
        self.teacher.save()
        exam = ExamSheet(title="test sheet", owner=self.teacher)
        exam.save()

    def test_questions_for_exam(self):
        exam = ExamSheet.objects.filter(owner=self.teacher).first()
        q_1 = Question.objects.create(text="test question", sheet=exam)
        q_2 = Question.objects.create(text="sec test question", sheet=exam)
        q_1.save()
        q_2.save()
        questions = exam.get_questions()
        self.assertEqual(len(questions), 2)


class TestQuestionModel(TestCase):
    def setUp(self):
        teacher = User(username="test_teacher", password="testzaq1@WSX")
        teacher.save()
        exam = ExamSheet(title="test sheet", owner=teacher)
        exam.save()
        self.question = Question(text="test question", sheet=exam)
        self.question.save()

    def test_ans_for_question(self):
        ans = CorrectAnswer.objects.create(question=self.question, ans_text="just a test answer")
        ans.save()
        sec_ans = CorrectAnswer.objects.create(question=self.question, ans_text="just another test answer")
        sec_ans.save()
        answers = self.question.get_answers()
        self.assertEqual(len(answers), 2)


class TestAtemptModel(TestCase):
    def setUp(self):
        teacher = User(username="test_teacher", password="testzaq1@WSX")
        teacher.save()
        exam = ExamSheet(title="test sheet", owner=teacher)
        exam.save()
        question = Question(text="test question", sheet=exam)
        question.save()
        corr_ans=CorrectAnswer(question=question, ans_text="testans")
        corr_ans.save()
        student = User(username="test student", password="testpassword@#$")
        student.save()
        self.attempt = Attempt(examinee=student, sheet=exam)
        self.attempt.save()

    def test_get_questions(self):
        questions = self.attempt.sheet.get_questions()
        self.assertEqual(len(questions), 1)


class TestGivenAnswerModel(TestCase):
    def setUp(self):
        teacher = User(username="test_teacher", password="testzaq1@WSX")
        teacher.save()
        exam = ExamSheet(title="test sheet", owner=teacher)
        exam.save()
        question = Question(text="test question", sheet=exam)
        question.save()
        corr_ans=CorrectAnswer(question=question, ans_text="test_ans")
        corr_ans.save()
        student = User(username="test student", password="testpassword@#$")
        student.save()
        attempt = Attempt(examinee=student, sheet=exam)
        attempt.save()
        self.give_ans_corr = Solution(attempt=attempt, to_question=question, given_text="test_ans")
        self.given_ans_wrong = Solution(attempt=attempt, to_question=question, given_text="no_ans")
        self.give_ans_corr.save()
        self.given_ans_wrong.save()

    def test_checking_answers(self):
        accuracy = self.give_ans_corr.check_accuracy()
        self.assertEqual(accuracy, True)


# Views test
class TestUserView(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user", password="testPassword")
        group = Group.objects.create(name="teachers")
        group.save()
        self.user.groups.add(group.id)
        self.user.save()
        self.factory = APIRequestFactory()

    def test_get(self):
        url = reverse("user-list")
        request = self.factory.get("")
        view = UserView.as_view({"get":"list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['group'], "teacher")


class TestExamSheet(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test_user", password="testPassword")
        group = Group.objects.create(name="teachers")
        group.save()
        user.groups.add(group.id)
        user.save()
        self.user_url = reverse("user-detail", args=(user.id,))
        self.client.force_login(user)

    def test_get_sheet(self):
        url = reverse("examsheet-list")
        response = self.client.get(url)
        

    def test_post_sheet(self):
        url = reverse("examsheet-list")
        data = {'title':"testTitle", 'owner':self.user_url}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], data['title'])


