from django.urls import path
from .views import (
    OrderListView, OrderDetailView, UpdateOrderStageView,
    IndividualListView, MeasurementListView, VendorRoleListView, VendorListView,
    PipelineStageListView, InvoiceListView
)

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order-stage/<int:pk>/update/', UpdateOrderStageView.as_view(), name='update_order_stage'),
    path('individuals/', IndividualListView.as_view(), name='individual_list'),
    path('measurements/', MeasurementListView.as_view(), name='measurement_list'),
    path('vendor-roles/', VendorRoleListView.as_view(), name='vendorrole_list'),
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('pipeline-stages/', PipelineStageListView.as_view(), name='pipelinestage_list'),
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
]
