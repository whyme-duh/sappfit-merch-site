from django import forms
from . models import Order

class TrackOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name' , 'email', 'order_id']