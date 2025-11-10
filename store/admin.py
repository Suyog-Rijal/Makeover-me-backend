from django.contrib import admin
from django.utils.html import format_html
from .models import Category, generate_unique_slug, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_preview']
    list_filter = ['created_on', 'updated_on']
    search_fields = ['name', 'slug']
    readonly_fields = ['created_on', 'updated_on']
    exclude = ['slug']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:25px; max-width:25px;" />', obj.image.url)
        return '-'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'unit_price', 'stock', 'is_active',]
    list_filter = ['is_active', 'is_featured', 'category']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    exclude = ['slug']

    inlines = [ProductImageInline]

