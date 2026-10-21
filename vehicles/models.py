from django.db import models


class Brand(models.Model):
	name = models.CharField(max_length=80, unique=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class Vehicle(models.Model):
	FUEL_CHOICES = [
		('Petrol', 'Petrol'),
		('Diesel', 'Diesel'),
		('Hybrid', 'Hybrid'),
		('Electric', 'Electric'),
		('Other', 'Other'),
	]

	name = models.CharField(max_length=120)
	brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='vehicles')
	price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
	seats = models.PositiveSmallIntegerField()
	fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Petrol')
	image = models.URLField(blank=True)
	description = models.TextField(blank=True)
	is_available = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['brand__name', 'name']

	def __str__(self):
		return f'{self.brand} {self.name}'
