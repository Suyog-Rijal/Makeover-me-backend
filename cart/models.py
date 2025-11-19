import uuid
from django.db import models
from account.models import User
from store.models import Product


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user}"


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user}'s cart"
