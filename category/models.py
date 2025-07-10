import uuid
from django.db import models
from django.utils.text import slugify
from filer.fields.image import FilerImageField


def generate_unique_category_slug(instance, new_slug=None):
	slug = new_slug or slugify(instance.name)
	ModelClass = instance.__class__
	qs = ModelClass.objects.filter(slug=slug).exclude(pk=instance.pk)
	if not qs.exists():
		return slug

	suffix = 1
	while True:
		new_slug = f"{slug}-{suffix}"
		if not ModelClass.objects.filter(slug=new_slug).exclude(pk=instance.pk).exists():
			return new_slug
		suffix += 1


def generate_unique_subcategory_slug(instance, new_slug=None):
	slug = new_slug or slugify(instance.name)
	qs = SubCategory.objects.filter(category=instance.category, slug=slug).exclude(pk=instance.pk)
	if not qs.exists():
		return slug

	suffix = 1
	while True:
		new_slug = f"{slug}-{suffix}"
		if not SubCategory.objects.filter(category=instance.category, slug=new_slug).exclude(pk=instance.pk).exists():
			return new_slug
		suffix += 1


class Category(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50, unique=True, db_index=True)
	description = models.TextField(null=True, blank=True)
	image = FilerImageField(
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="category_images")
	is_active = models.BooleanField(default=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

	def save(self, *args, **kwargs):
		self.name = self.name.strip().title()
		self.slug = generate_unique_category_slug(self)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name


class SubCategory(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50)
	description = models.TextField(null=True, blank=True)
	image = FilerImageField(
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="subcategory_images"
	)
	is_active = models.BooleanField(default=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = (
			('category', 'name'),
			('category', 'slug'),
		)
		ordering = ['name']
		verbose_name = 'SubCategory'
		verbose_name_plural = 'SubCategories'

	def save(self, *args, **kwargs):
		self.name = self.name.strip().title()
		self.slug = generate_unique_subcategory_slug(self)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name
