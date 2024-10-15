from rest_framework.pagination import PageNumberPagination


class EmployeePagination(PageNumberPagination):
    page_size = 100
