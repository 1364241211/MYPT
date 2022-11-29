from rest_framework.pagination import PageNumberPagination


class customersPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'page'
    page_size = 30


class teachersPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'page'
    page_size = 30
