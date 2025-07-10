from rest_framework import serializers

from category.models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
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
	subcategories = SubCategorySerializer(many=True, read_only=True)

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
