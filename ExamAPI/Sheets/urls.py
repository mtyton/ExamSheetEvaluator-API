from django.urls import path, include
from rest_framework import routers
from.views import ExamSheetView, QuestionView, CorrectAnswerView, ExamUserView
from .views import AttemptView, SolutionView, PointView


router = routers.DefaultRouter()
router.register("examuser", ExamUserView, basename="examuser")
router.register("examsheet", ExamSheetView, basename="examsheet")
router.register("question", QuestionView, basename="question")
router.register("correct_answer", CorrectAnswerView, basename="correctanswer")

router.register("attempt", AttemptView, basename="attempt")
router.register("solution", SolutionView, basename="solution")
router.register("point", PointView, basename="point")

urlpatterns = [
    path('', include(router.urls)),
]