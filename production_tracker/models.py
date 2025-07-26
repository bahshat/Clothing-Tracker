from django.db import models
from django.contrib.postgres.fields import ArrayField

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField(null=True, blank=True)
    address = models.TextField(blank=True)

class Measurement(models.Model):
    id = models.AutoField(primary_key=True)
    MEASUREMENT_CHOICES = [
        ('Pant', 'Pant'),
        ('Shirt', 'Shirt'),
        ('Suite', 'Suite'),
        # Add more as needed
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    measurement_type = models.CharField(max_length=20, choices=MEASUREMENT_CHOICES)
    value = models.JSONField(blank=True, null=True, help_text="Stores measurement values in JSON format.")

class VendorRole(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=10)

class Vendor(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.ForeignKey(VendorRole, on_delete=models.CASCADE)
    phone_numbers = ArrayField(models.BigIntegerField(), blank=True, null=True, default=list, help_text="List of contact phone numbers for the vendor.")
    address = models.TextField(blank=True)
    remark = models.TextField(blank=True, help_text="Any additional remarks about the vendor.")

class PipelineStage(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_placed_on = models.DateField()
    status = models.CharField(max_length=10)
    completion_date = models.DateField(null=True, blank=True, help_text="Date when the order was completed.")
    amount = models.IntegerField(default=0, help_text="Total calculated amount for the order. Stored as integer, e.g., in cents/paise.")
    invoice = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

class OrderStage(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE)
    assigned_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10)

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    total_amount = models.IntegerField(default=0, help_text="Total amount of the invoice. Stored as integer, e.g., in cents/paise.")
    paid_on_date = models.DateField(null=True, blank=True)
    paid = models.BooleanField(default=False)

class Particulars(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='particulars')
    name = models.CharField(max_length=20, help_text="Name or description of the particular item.")
    details = models.CharField(max_length=100, blank=True, help_text="Additional details about the particular item.")
    amount = models.IntegerField(help_text="Amount for this particular item. Stored as integer, e.g., in cents/paise.")
