from django.urls import path
from .views import (
    DashboardView,
    OrderListView, OrderDetailView, UpdateOrderStageView, OrderCreateView,
    CustomerListView, CustomerCreateView,
    MeasurementListView, MeasurementCreateView,
    VendorRoleListView, VendorListView,
    PipelineStageListView, InvoiceListView,
    CustomLoginView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/new/', OrderCreateView.as_view(), name='order_new'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order-stage/<int:pk>/update/', UpdateOrderStageView.as_view(), name='update_order_stage'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/new/', CustomerCreateView.as_view(), name='customer_new'),
    path('measurements/', MeasurementListView.as_view(), name='measurement_list'),
    path('measurements/new/', MeasurementCreateView.as_view(), name='measurement_new'),
    path('vendor-roles/', VendorRoleListView.as_view(), name='vendorrole_list'),
    path('vendors/', VendorListView.as_view(), name='vendor_list'),
    path('pipeline-stages/', PipelineStageListView.as_view(), name='pipelinestage_list'),
    path('invoices/', InvoiceListView.as_view(), name='invoice_list'),
]