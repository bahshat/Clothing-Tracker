from django.db import models

class Individual(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class Measurement(models.Model):
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    measurement_type = models.CharField(max_length=50)
    value = models.FloatField()
    date_recorded = models.DateField()

class VendorRole(models.Model):
    name = models.CharField(max_length=100)

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(VendorRole, on_delete=models.CASCADE)

class PipelineStage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Individual, on_delete=models.CASCADE)
    order_date = models.DateField()
    status = models.CharField(max_length=50)

class OrderStage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stage = models.ForeignKey(PipelineStage, on_delete=models.CASCADE)
    assigned_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField()
    date_due = models.DateField()
    paid = models.BooleanField(default=False)