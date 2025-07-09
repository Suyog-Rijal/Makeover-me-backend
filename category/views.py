from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet

from .models import Category
from .serializers import CategorySerializer


@extend_schema_view(
	list=extend_schema(
		summary="List all categories",
		tags=["Category"]
	),
	retrieve=extend_schema(
		summary="Retrieve a category by slug",
		tags=["Category"]
	)
)
class CategoryViewSet(ModelViewSet):
	http_method_names = ['get']
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	lookup_field = 'slug'
