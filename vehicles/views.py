from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from contact.models import SiteContent

from .forms import VehicleFilterForm
from .models import Vehicle


def home(request):
	site_content = SiteContent.objects.first()
	featured_vehicles = Vehicle.objects.filter(
		is_featured=True, is_available=True
	).select_related('brand')[:6]
	return render(request, 'home.html', {
		'site_content': site_content,
		'featured_vehicles': featured_vehicles,
	})


def vehicle_list(request):
	filters = VehicleFilterForm(request.GET or None)
	vehicles = Vehicle.objects.select_related('brand').all()
	if filters.is_valid():
		values = filters.cleaned_data
		if values['brand']:
			vehicles = vehicles.filter(brand=values['brand'])
		if values['min_price'] is not None:
			vehicles = vehicles.filter(price_per_day__gte=values['min_price'])
		if values['max_price'] is not None:
			vehicles = vehicles.filter(price_per_day__lte=values['max_price'])
		if values['seats'] is not None:
			vehicles = vehicles.filter(seats=values['seats'])
		if values['available']:
			vehicles = vehicles.filter(is_available=values['available'] == 'yes')
	page_obj = Paginator(vehicles, 9).get_page(request.GET.get('page'))
	return render(request, 'vehicles/list.html', {
		'filters': filters,
		'vehicles': page_obj,
	})


def vehicle_detail(request, pk):
	vehicle = get_object_or_404(
		Vehicle.objects.select_related('brand'), pk=pk
	)
	return render(request, 'vehicles/detail.html', {'vehicle': vehicle})
