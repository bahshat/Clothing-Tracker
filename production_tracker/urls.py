from django.urls import path
from .views import OrderListView, OrderDetailView, UpdateOrderStageView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order-stage/<int:pk>/update/', UpdateOrderStageView.as_view(), name='update_order_stage'),
]