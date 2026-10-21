from django.contrib import admin

from .models import Contact, SiteContent, Subscriber


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ['subject', 'name', 'email', 'is_read', 'created_at']
	list_filter = ['is_read', 'created_at']
	search_fields = ['name', 'email', 'subject', 'message']
	list_editable = ['is_read']
	readonly_fields = ['created_at']


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
	list_display = ['email', 'is_active', 'created_at']
	list_filter = ['is_active', 'created_at']
	search_fields = ['email']
	list_editable = ['is_active']
	readonly_fields = ['created_at']


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
	list_display = ['home_heading', 'contact_email', 'contact_phone', 'updated_at']
	readonly_fields = ['updated_at']

	def has_add_permission(self, request):
		return not SiteContent.objects.exists()

	def has_delete_permission(self, request, obj=None):
		return False
