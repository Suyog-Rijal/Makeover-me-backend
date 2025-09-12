from django.db import models, transaction


def generate_id(model):
    prefix_map = {Region: 'R', City: 'C', Area: 'A'}
    model_prefix = prefix_map[model]
    with transaction.atomic():
        try:
            latest_entry = model.objects.select_for_update().latest('id')
            last_id = latest_entry.id
            number = int(last_id[1:])
            if number < 9999:
                new_number = number + 1
                new_id = f"{model_prefix}{new_number:04d}"
            else:
                return None
            return new_id
        except model.DoesNotExist:
            return f"{model_prefix}0001"

# ----------------------------
# Models
# ----------------------------
class Region(models.Model):
    id = models.CharField(max_length=5, primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(Region)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name}"


class City(models.Model):
    id = models.CharField(max_length=5, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='cities', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'region')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(City)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Area(models.Model):
    id = models.CharField(max_length=5, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, related_name='areas', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'city')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(Area)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name}"
