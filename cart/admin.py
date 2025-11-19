from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'total')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'unit_price', 'quantity', 'subtotal', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
