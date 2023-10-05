from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20  # Set the number of items per page
    page_size_query_param = 'page_size'  # Optional, allows changing page size via query parameter
    max_page_size = 100  # Optional, maximum page size