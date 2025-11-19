from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from cart.models import Cart, CartItem
from cart.serializer import AddToCartSerializer, RemoveFromCartSerializer, GetAllCartItemsSerializer


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AddToCartSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "cart_item_id": {"type": "string", "format": "uuid"},
                    "product": {"type": "string", "format": "uuid"},
                    "quantity": {"type": "integer"},
                    "price": {"type": "string"},
                    "subtotal": {"type": "string"}
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "product": {"type": "array", "items": {"type": "string"}},
                    "quantity": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        tags=['Cart']
    )
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        cart = Cart.objects.get_or_create(user=request.user)[0]
        existing_items = CartItem.objects.filter(cart=cart, product=serializer.validated_data['product'])
        if existing_items.exists():
            item = existing_items.first()
            item.quantity += serializer.validated_data['quantity']
            item.unit_price = item.product.unit_price
            item.save()
        else:
            item = CartItem.objects.create(
                cart=cart,
                product=serializer.validated_data['product'],
                quantity=serializer.validated_data['quantity'],
                unit_price=serializer.validated_data['product'].unit_price
            )

        return Response({
            "message": "Product added to cart successfully",
            "cart_item_id": str(item.id),
            "product": str(item.product.id),
            "quantity": item.quantity,
            "unit_price": str(item.unit_price),
            "subtotal": str(item.subtotal)
        }, status=status.HTTP_201_CREATED)


class RemoveFromCartApiView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RemoveFromCartSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                }
            }
        },
        tags=['Cart']
    )
    def post(self, request):
        serializer = RemoveFromCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        product_id = serializer.validated_data['product_id']
        try:
            cart = get_object_or_404(Cart, user=request.user)
            if not cart:
                return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
            cart_item = get_object_or_404(CartItem, cart=cart, product__id=product_id)
            if not cart_item:
                return Response({"detail": "Product not found in cart."}, status=status.HTTP_404_NOT_FOUND)
            cart_item.delete()
            return Response({"message": "Product removed from cart successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Something went wrong. Please try again after some time."},
                            status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={
        200: OpenApiResponse(response=GetAllCartItemsSerializer(many=True)),
        401: {
            "type": "object",
            "properties": {
                "detail": {"type": "string"}
            }
        }
    },
    tags=['Cart']
)
class GetAllCart(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetAllCartItemsSerializer

    def get_queryset(self):
        cart = getattr(self.request.user, 'cart', None)
        if cart:
            return CartItem.objects.filter(cart=cart)
        return CartItem.objects.none()
