import os
import django
import random
import uuid
from faker import Faker

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from store.models import Category, Product
from store.models import generate_unique_slug  # Your existing function
from django.utils.text import slugify

fake = Faker()

categories = list(Category.objects.all())

# Randomly exclude 0-2 categories from getting products
categories_with_products = random.sample(categories, k=len(categories) - random.randint(0, 2))

for _ in range(200):
    category = random.choice(categories_with_products)
    name = fake.unique.catch_phrase()

    # Randomly include a preview image or not
    preview = f"https://picsum.photos/seed/{uuid.uuid4().hex}/500/500" if random.choice([True, False]) else None
    description = fake.paragraph(nb_sentences=3) if random.choice([True, False]) else ''
    unit_price = round(random.uniform(5.0, 500.0), 2)
    stock = random.randint(0, 100)
    is_featured = random.choice([True, False])
    rating = round(random.uniform(0, 5), 1)

    # Step 1: create Product instance WITHOUT saving
    product = Product(
        category=category,
        name=name,
        preview=preview,
        description=description,
        unit_price=unit_price,
        stock=stock,
        is_featured=is_featured,
        rating=rating,
        is_active=True
    )

    # Step 2: generate unique slug
    product.slug = generate_unique_slug(product, field_name='name', slug_field='slug', max_length=255)

    # Step 3: save the product
    product.save()

print("✅ 200 products generated with realistic preview images and unique slugs!")
