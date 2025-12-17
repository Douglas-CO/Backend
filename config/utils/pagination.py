# utils/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # valor por defecto
    page_size_query_param = 'page_size'  # permite cambiarlo desde query param

    def get_paginated_response(self, data):
        return Response({
            "status": 200,
            "message": "Elementos paginados correctamente",
            "data": {
                "meta": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "count": self.page.paginator.count,
                    "total_pages": self.page.paginator.num_pages
                },
                "items": data
            }
        })
