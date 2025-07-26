from django import forms
from .models import OrderStage, Vendor, Order, Customer, Measurement, PipelineStage, Particulars

class OrderStageUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderStage
        fields = ['status', 'assigned_vendor']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'order_placed_on', 'status']
        widgets = {
            'order_placed_on': forms.DateInput(attrs={'type': 'date'})
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['customer', 'measurement_type', 'value']

class OrderStageCreateForm(forms.ModelForm):
    class Meta:
        model = OrderStage
        fields = ['stage', 'assigned_vendor', 'start_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'})
        }
