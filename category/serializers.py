from rest_framework import serializers

from category.models import Category, SubCategory


class SimpleSubCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = SubCategory
		fields = (
			'id',
			'name',
			'slug',
			'description',
			'image',
		)


class CategorySerializer(serializers.ModelSerializer):
	subcategories = SimpleSubCategorySerializer(many=True, read_only=True)

	class Meta:
		model = Category
		fields = (
			'id',
			'name',
			'slug',
			'description',
			'image',
			'subcategories'
		)
