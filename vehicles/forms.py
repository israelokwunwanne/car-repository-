from django import forms

from .models import Brand


class VehicleFilterForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.none(), required=False)
    min_price = forms.DecimalField(required=False, min_value=0, decimal_places=2)
    max_price = forms.DecimalField(required=False, min_value=0, decimal_places=2)
    seats = forms.IntegerField(required=False, min_value=1)
    available = forms.ChoiceField(
        required=False,
        choices=[('', 'Any availability'), ('yes', 'Available'), ('no', 'Unavailable')],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        minimum = cleaned_data.get('min_price')
        maximum = cleaned_data.get('max_price')
        if minimum is not None and maximum is not None and minimum > maximum:
            self.add_error('max_price', 'Maximum price must be at least the minimum price.')
        return cleaned_data