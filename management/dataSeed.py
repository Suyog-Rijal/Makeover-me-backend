import os
import django
import random

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from store.models import Product

products = Product.objects.all()

if not products:
    print("❌ No products found!")
    exit()

print(f"🟢 Updating {products.count()} existing products...")

def chance(prob):
    """Return True based on probability (0.0 – 1.0)."""
    return random.random() < prob

for product in products:
    # Weighted TRUE/FALSE values
    flags = {
        "is_featured": chance(0.30),            # 30% chance
        "is_flash_sale": chance(0.10),          # 10% chance
        "is_product_of_the_day": chance(0.05),  # 5% chance
        "is_best_seller": chance(0.15),         # 15% chance
        "is_attractive_offer": chance(0.20),    # 20% chance
    }

    # Ensure at least one flag is True
    if not any(flags.values()):
        random_key = random.choice(list(flags.keys()))
        flags[random_key] = True

    # Assign values to product
    for key, value in flags.items():
        setattr(product, key, value)

    product.save()

print("🎉 Successfully updated all products with random promotional values!")
