from django.test import TestCase
from django.contrib.auth.models import Group, User
from .models import ExamSheet, Question, Solution, Point
from rest_framework.test import APIRequestFactory, APITestCase
from django.urls import reverse
from .views import UserView


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

    def test_get_solutions(self):
        student = User(username="test_student", password="testzaq1@WSX")
        student.save()
        solution = Solution(examinee=student, to_question=self.question, given_text="test ans")
        sec_solution = Solution(examinee=student, to_question=self.question, given_text="test ans")
        solution.save()
        sec_solution.save()
        solutions = self.question.get_solutions()
        self.assertEqual(len(solutions), 2)

    def test_get_solutions_for_student(self):
        student = User(username="test_student", password="testzaq1@WSX")
        student.save()
        solution = Solution(examinee=student, to_question=self.question, given_text="test ans")
        sec_solution = Solution(examinee=student, to_question=self.question, given_text="test ans")
        solution.save()
        sec_solution.save()
        solutions = self.question.get_solutions_for_student(student)
        self.assertEqual(len(solutions), 2)


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


class TestExamSheetView(APITestCase):
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
        self.assertEqual(response.status_code, 200)

    def test_post_sheet(self):
        url = reverse("examsheet-list")
        data = {'title':"testTitle", 'owner':self.user_url}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], data['title'])


class TestQuestionView(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test_teacher", password="testPassword")
        group = Group.objects.create(name="teachers")
        group.save()
        user.groups.add(group.id)
        user.save()
        self.client.force_login(user)
        exam = ExamSheet.objects.create(title="test_title", owner=user)
        self.exam_url = reverse("examsheet-detail", args=(exam.id,))

    def test_get_question(self):
        url = reverse("question-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_question(self):
        url = reverse("question-list")
        data = {'text': 'test_text', 'sheet': self.exam_url}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['text'], data['text'])


class TestSolutionView(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test_student", password="testPassword")
        group = Group.objects.create(name="students")
        group.save()
        user.groups.add(group.id)
        user.save()
        self.client.force_login(user)
        exam = ExamSheet.objects.create(title="test_title", owner=user)
        question = Question.objects.create(text="testText", sheet=exam)
        question.save()
        self.question_url = reverse("question-detail", args=(question.id,))
        self.user_url = reverse("user-detail", args=(user.id,))

    def test_get_question(self):
        url = reverse("solution-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_question(self):
        url = reverse("solution-list")
        data = {'to_question': self.question_url, 'examinee': self.user_url, 'given_text': 'test_text'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['given_text'], data['given_text'])


class TestPointView(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test_student", password="testPassword")
        group = Group.objects.create(name="teachers")
        group.save()
        student_group = Group.objects.create(name="students")
        student_group.save()
        user.groups.add(group.id)
        user.groups.add(student_group.id)
        user.save()
        self.client.force_login(user)
        exam = ExamSheet.objects.create(title="test_title", owner=user)
        question = Question.objects.create(text="testText", sheet=exam)
        question.save()
        self.solution = Solution.objects.create(to_question=question, examinee=user, given_text="testText")
        self.solution.save()

    def test_get_point(self):
        url = reverse("point-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_point(self):
        url = reverse("point-list")
        data = {'answer':self.solution.id, 'points':1}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['points'], data['points'])


class GradeView(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test_student", password="testPassword")
        group = Group.objects.create(name="teachers")
        group.save()
        student_group = Group.objects.create(name="students")
        student_group.save()
        user.groups.add(group.id)
        user.groups.add(student_group.id)
        user.save()
        self.client.force_login(user)
        exam = ExamSheet.objects.create(title="test_title", owner=user)
        exam.save()
        self.exam_url = reverse("examsheet-detail", args=(exam.id,))
        self.user_url = reverse("user-detail", args=(user.id,))

    def test_get_grade(self):
        url = reverse("grade-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_grade(self):
        url = reverse("grade-list")
        data = {'sheet': self.exam_url, 'user': self.user_url, 'mark': 6}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['mark'], data['mark'])
