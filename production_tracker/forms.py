from django import forms
from .models import OrderStage, Vendor, Order, Individual, Measurement

class OrderStageUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderStage
        fields = ['status', 'assigned_vendor']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'customer', 'order_date', 'status']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'})
        }

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ['name', 'email', 'phone']

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['individual', 'measurement_type', 'value', 'date_recorded']
        widgets = {
            'date_recorded': forms.DateInput(attrs={'type': 'date'})
        }