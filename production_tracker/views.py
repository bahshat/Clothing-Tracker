from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Order, OrderStage
from .forms import OrderStageUpdateForm
from datetime import date

class OrderListView(ListView):
    model = Order
    template_name = 'production_tracker/order_list.html'
    context_object_name = 'orders'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'production_tracker/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stage_update_form'] = OrderStageUpdateForm()
        return context

class UpdateOrderStageView(View):
    def post(self, request, pk):
        order_stage = get_object_or_404(OrderStage, pk=pk)
        form = OrderStageUpdateForm(request.POST, instance=order_stage)
        if form.is_valid():
            updated_stage = form.save(commit=False)
            if updated_stage.status == 'Completed':
                updated_stage.end_date = date.today()
                
                # Get the next stage in the sequence
                next_stage = OrderStage.objects.filter(
                    order=updated_stage.order, 
                    stage__id=updated_stage.stage.id + 1
                ).first()

                if next_stage:
                    next_stage.status = 'In Progress'
                    next_stage.save()

            updated_stage.save()
        return redirect('order_detail', pk=order_stage.order.pk)
