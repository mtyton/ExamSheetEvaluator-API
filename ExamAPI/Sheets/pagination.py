from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class NewLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50