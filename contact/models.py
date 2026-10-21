from django.db import models


class Contact(models.Model):
	name = models.CharField(max_length=120)
	email = models.EmailField()
	subject = models.CharField(max_length=160)
	message = models.TextField(max_length=3000)
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'{self.subject} from {self.name}'


class Subscriber(models.Model):
	email = models.EmailField(unique=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.email


class SiteContent(models.Model):
	home_heading = models.CharField(max_length=120, default='Find your next drive')
	home_intro = models.TextField(blank=True)
	contact_email = models.EmailField(blank=True)
	contact_phone = models.CharField(max_length=40, blank=True)
	contact_address = models.CharField(max_length=255, blank=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'site content'
		verbose_name_plural = 'site content'

	def __str__(self):
		return 'Website and contact details'
