from django.db import models
from django.utils.text import slugify
from filer.fields.image import FilerImageField
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

def generate_unique_slug(instance, field_name='name', slug_field='slug', max_length=120):
    base_value = getattr(instance, field_name, '') or 'item'
    base_slug = slugify(base_value)[:max_length] or 'item'
    slug = base_slug
    counter = 1

    ModelClass = instance.__class__
    while ModelClass.objects.filter(**{slug_field: slug}).exclude(pk=instance.pk).exists():
        suffix = f"-{counter}"
        slug = base_slug[:max_length - len(suffix)] + suffix
        counter += 1

    return slug


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name='category_images')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self, field_name='name', slug_field='slug', max_length=120)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    preview = models.URLField(max_length=500, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    is_flash_sale = models.BooleanField(default=False)
    is_product_of_the_day = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_attractive_offer = models.BooleanField(default=False)


    rating = models.FloatField(default=0.0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(self, field_name='name', slug_field='slug', max_length=255)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name='product_images')

    def save(self, *arge, **kwargs):
        self.alt_text = f'{self.product.name} image'
        super().save(*arge, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"
