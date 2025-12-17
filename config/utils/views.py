# utils/views.py
from rest_framework.generics import ListAPIView
from utils.pagination import CustomPagination


class GenericListView(ListAPIView):
    pagination_class = CustomPagination

    # estos atributos los defines en cada vista concreta
    queryset = None
    serializer_class = None
