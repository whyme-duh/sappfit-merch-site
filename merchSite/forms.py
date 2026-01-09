from django import forms
from . models import Order

class TrackOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'order_id']