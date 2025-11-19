from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, FlashSalesListView, ProductOfTheDayListView, BestSellerListView, AttractiveOfferListView
from django.urls import path

router = DefaultRouter()

router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('flash-sales/', FlashSalesListView.as_view(), name='flash-sales'),
    path('product-of-the-day/', ProductOfTheDayListView.as_view(), name='product-of-the-day'),
    path('best-sellers/', BestSellerListView.as_view(), name='best-sellers'),
    path('attractive-offers/', AttractiveOfferListView.as_view(), name='attractive-offers'),
] + router.urls