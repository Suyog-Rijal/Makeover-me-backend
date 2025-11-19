from rest_framework import serializers

from store.models import Product
from store.serializers import CategorySerializer
from .models import CartItem

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('product', 'quantity')

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        product = self.initial_data.get('product')
        if product:
            try:
                product_instance = self.Meta.model._meta.get_field('product').related_model.objects.get(id=product)
                if value > product_instance.stock:
                    raise serializers.ValidationError("Requested quantity exceeds available stock.")
            except self.Meta.model._meta.get_field('product').related_model.DoesNotExist:
                raise serializers.ValidationError("Product does not exist.")

        return value


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()


from rest_framework import serializers
from .models import CartItem
from store.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GetAllCartItemsSerializer(serializers.ModelSerializer):
    class ProductInlineSerializer(serializers.ModelSerializer):
        category = CategorySerializer()

        class Meta:
            model = Product
            fields = (
                'id',
                'name',
                'slug',
                'description',
                'unit_price',
                'stock',
                'preview',
                'category',
            )

    product = ProductInlineSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'unit_price', 'quantity', 'subtotal')
