from pkgutil import extend_path

from django.urls import path
from rest_framework.routers import DefaultRouter
from category.views import CategoryViewSet

router = DefaultRouter()
router.register('', CategoryViewSet, basename='category')

urlpatterns = [

]

urlpatterns += router.urls

