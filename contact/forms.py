from django import forms

from .models import Contact, Subscriber


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {'message': forms.Textarea(attrs={'rows': 5})}


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']