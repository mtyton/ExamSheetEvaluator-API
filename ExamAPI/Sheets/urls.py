from django.urls import path, include
from rest_framework import routers
from.views import ExamSheetView, QuestionView, UserView
from .views import SolutionView, PointView, GradeView


router = routers.DefaultRouter()

router.register("user", UserView, basename="user")

router.register("examsheet", ExamSheetView, basename="examsheet")
router.register("question", QuestionView, basename="question")

router.register("solution", SolutionView, basename="solution")
router.register("point", PointView, basename="point")
router.register("grade", GradeView, basename="grade")

urlpatterns = [
    path('', include(router.urls)),
]