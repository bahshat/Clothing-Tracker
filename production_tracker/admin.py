from django.contrib import admin
from .models import (
    Individual, Measurement, VendorRole, Vendor, PipelineStage, Order, OrderStage, Invoice
)

class OrderStageInline(admin.TabularInline):
    model = OrderStage
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'order_date', 'status')
    inlines = [OrderStageInline]

@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')

admin.site.register(Measurement)
admin.site.register(VendorRole)
admin.site.register(PipelineStage)
admin.site.register(OrderStage)
admin.site.register(Invoice)