from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm, SubscriberForm
from .models import SiteContent


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your message has been sent.')
			return redirect('contact:contact')
	else:
		form = ContactForm()
	return render(request, 'contact/contact.html', {
		'form': form,
		'site_content': SiteContent.objects.first(),
	})


def subscribe(request):
	if request.method == 'POST':
		form = SubscriberForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'You are now subscribed.')
		else:
			messages.error(request, 'Enter a valid email address that is not already subscribed.')
	return redirect(request.META.get('HTTP_REFERER') or 'home')
