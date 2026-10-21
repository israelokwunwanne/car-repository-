from django.test import TestCase
from django.urls import reverse

from .models import Contact, SiteContent, Subscriber


class ContactWorkflowTests(TestCase):
	def test_contact_message_is_saved_and_contact_details_are_displayed(self):
		SiteContent.objects.create(contact_email='hello@example.com')
		response = self.client.post(reverse('contact:contact'), {
			'name': 'A Customer',
			'email': 'customer@example.com',
			'subject': 'Vehicle question',
			'message': 'Please share more details.',
		})
		self.assertRedirects(response, reverse('contact:contact'))
		self.assertEqual(Contact.objects.count(), 1)
		self.assertContains(self.client.get(reverse('contact:contact')), 'hello@example.com')

	def test_invalid_contact_message_is_not_saved(self):
		response = self.client.post(reverse('contact:contact'), {'email': 'not-an-email'})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Contact.objects.count(), 0)

	def test_subscriber_can_join_once(self):
		url = reverse('contact:subscribe')
		self.client.post(url, {'email': 'updates@example.com'})
		self.client.post(url, {'email': 'updates@example.com'})
		self.assertEqual(Subscriber.objects.count(), 1)
