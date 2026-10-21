from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Brand, Vehicle


class VehicleCatalogueTests(TestCase):
	def setUp(self):
		self.brand = Brand.objects.create(name='Nissan')
		self.other_brand = Brand.objects.create(name='Toyota')
		self.vehicle = Vehicle.objects.create(
			name='Leaf', brand=self.brand, price_per_day=Decimal('75.00'),
			seats=5, fuel_type='Electric', is_featured=True,
		)

	def test_catalogue_filters_brand_price_seats_and_availability(self):
		Vehicle.objects.create(
			name='Micra', brand=self.brand, price_per_day=Decimal('45.00'),
			seats=4, is_available=False,
		)
		Vehicle.objects.create(
			name='Corolla', brand=self.other_brand, price_per_day=Decimal('75.00'),
			seats=5,
		)
		response = self.client.get(reverse('vehicles:list'), {
			'brand': self.brand.pk,
			'min_price': '70',
			'max_price': '80',
			'seats': '5',
			'available': 'yes',
		})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context['vehicles'].object_list), [self.vehicle])

	def test_catalogue_paginates_and_detail_is_public(self):
		for index in range(10):
			Vehicle.objects.create(
				name=f'Car {index}', brand=self.brand,
				price_per_day=Decimal('60.00'), seats=5,
			)
		listing = self.client.get(reverse('vehicles:list'))
		detail = self.client.get(reverse('vehicles:detail', args=[self.vehicle.pk]))
		self.assertEqual(listing.context['vehicles'].paginator.num_pages, 2)
		self.assertEqual(detail.status_code, 200)
		self.assertContains(detail, reverse('bookings:create'))

	def test_home_shows_featured_available_vehicles(self):
		Vehicle.objects.create(
			name='Unavailable', brand=self.brand, price_per_day=Decimal('50.00'),
			seats=5, is_featured=True, is_available=False,
		)
		response = self.client.get(reverse('home'))
		self.assertEqual(list(response.context['featured_vehicles']), [self.vehicle])
