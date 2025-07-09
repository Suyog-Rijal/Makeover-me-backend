from django.contrib import admin
from django.utils.html import format_html

from .models import Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_active', 'image_preview')
	search_fields = ('name', 'slug')
	list_filter = ('is_active', 'created_at')
	prepopulated_fields = {"slug": ("name",)}

	class SubCategoryInline(admin.TabularInline):
		model = SubCategory
		extra = 1
		fields = ('name', 'slug', 'is_active')
		prepopulated_fields = {"slug": ("name",)}

	inlines = [SubCategoryInline]

	def image_preview(self, obj):
		if obj.image:
			return format_html('<img src="%s" height="30px" width="30px" />' % obj.image.url)
		return format_html('<span>-</span>')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'slug', 'is_active', 'created_at', 'updated_at')
	search_fields = ('name', 'slug', 'category__name')
	list_filter = ('category', 'is_active', 'created_at')
	prepopulated_fields = {"slug": ("name",)}
