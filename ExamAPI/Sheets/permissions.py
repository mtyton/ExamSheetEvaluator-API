from rest_framework.permissions import BasePermission, SAFE_METHODS


class ExamSheetPermission(BasePermission):
    """
    Permission for ExamSheet allows to readonly if you are not the owner
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.groups.filter(name='teachers')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.owner


class QuestionPermission(BasePermission):
    """
    If yu are not the owner of any examsheet you can't add question to any
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.groups.filter(name='teachers')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.sheet.owner


class IsExamineeOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.examinee


class PointPermissions(BasePermission):
    """
    You can only add points if answer has been given to exam you own
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.groups.filter(name='teachers')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.answer.question.sheet.owner


class GradePermissions(BasePermission):
    """
    You can only give grades if you are a teacher and only for exams you own
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.groups.filter(name='teachers')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.sheet.owner