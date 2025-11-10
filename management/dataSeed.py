import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # <-- replace with your settings module
django.setup()

from store.models import Category, Product

fake = Faker()

categories = list(Category.objects.all())
for _ in range(100):
    category = random.choice(categories)
    name = fake.unique.word().title()
    description = fake.text(max_nb_chars=200)
    unit_price = round(random.uniform(10.0, 500.0), 2)
    stock = random.randint(0, 100)
    rating = round(random.uniform(0.0, 5.0), 1)

    Product.objects.create(
        category=category,
        name=name,
        description=description,
        unit_price=unit_price,
        stock=stock,
        rating=rating
    )

print("✅ 100 fake products created!")
