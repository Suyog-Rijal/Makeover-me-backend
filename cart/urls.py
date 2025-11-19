from django.urls import path
from .views import AddToCartView, RemoveFromCartApiView, GetAllCart

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/', RemoveFromCartApiView.as_view(), name='remove-from-cart'),
    path('', GetAllCart.as_view(), name='get-all-cart'),
]