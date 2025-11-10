from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from api.filters import ProductCategoryFilter
from api.pagination import ProductResultsPagination
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


@extend_schema_view(
    list=extend_schema(
        auth=[],
        tags=['Products'],
    ),
    retrieve=extend_schema(
        auth=[],
        tags=['Products'],
    )
)
class ProductViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductCategoryFilter
    search_fields = ['name', 'description']
    pagination_class = ProductResultsPagination


@extend_schema_view(
    list=extend_schema(
        auth=[],
        tags=['Category'],
    ),
    retrieve=extend_schema(
        auth=[],
        tags=['Category'],
    )
)
class CategoryViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'