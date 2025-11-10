from api.utils import get_image_url
from .models import ProductImage, Product, Category
from rest_framework import serializers

class ImageURLField(serializers.Field):
    def to_representation(self, value):
        if not value or not hasattr(value, 'url'):
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(value.url)
        return value.url

class SimpleCategorySerializer(serializers.ModelSerializer):
    image = ImageURLField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']


class ProductSerializer(serializers.ModelSerializer):
    class ProductImageSerializer(serializers.ModelSerializer):
        image = ImageURLField()
        class Meta:
            model = ProductImage
            fields = ['image',]

    category = SimpleCategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'unit_price',
            'stock',
            'is_featured',
            'rating',
            'category',
            'images'
        ]

class CategorySerializer(serializers.ModelSerializer):
    image = ImageURLField()
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'image'
        ]