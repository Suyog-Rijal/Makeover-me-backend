from django.urls import path

from category.views import CategoryViewSet
from rest_framework.routers import DefaultRouter
from category.views import CategoryViewSet

router = DefaultRouter()
router.register('', CategoryViewSet, basename='category')

urlpatterns = [
]

urlpatterns += router.urls

