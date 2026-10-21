from django.contrib import admin

from .models import Brand, Vehicle


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']
	ordering = ['name']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
	list_display = ['name', 'brand', 'price_per_day', 'seats', 'fuel_type', 'is_available', 'is_featured']
	list_filter = ['brand', 'fuel_type', 'seats', 'is_available', 'is_featured']
	search_fields = ['name', 'brand__name', 'description']
	list_editable = ['price_per_day', 'is_available', 'is_featured']
