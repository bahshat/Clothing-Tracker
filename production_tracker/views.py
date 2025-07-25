from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import Order, OrderStage, Individual, Measurement, VendorRole, Vendor, PipelineStage, Invoice
from .forms import OrderStageUpdateForm, OrderForm, IndividualForm, MeasurementForm
from datetime import date

class DashboardView(TemplateView):
    template_name = 'production_tracker/dashboard.html'

class OrderListView(ListView):
    model = Order
    template_name = 'production_tracker/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

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
                # Assuming stages are ordered by their ID for simplicity in this example
                next_stage = OrderStage.objects.filter(
                    order=updated_stage.order, 
                    stage__id__gt=updated_stage.stage.id
                ).order_by('stage__id').first()

                if next_stage:
                    next_stage.status = 'In Progress'
                    next_stage.save()

            updated_stage.save()
        return redirect('order_detail', pk=order_stage.order.pk)

class IndividualListView(ListView):
    model = Individual
    template_name = 'production_tracker/individual_list.html'
    context_object_name = 'individuals'

class MeasurementListView(ListView):
    model = Measurement
    template_name = 'production_tracker/measurement_list.html'
    context_object_name = 'measurements'

class VendorRoleListView(ListView):
    model = VendorRole
    template_name = 'production_tracker/vendorrole_list.html'
    context_object_name = 'vendor_roles'

class VendorListView(ListView):
    model = Vendor
    template_name = 'production_tracker/vendor_list.html'
    context_object_name = 'vendors'

class PipelineStageListView(ListView):
    model = PipelineStage
    template_name = 'production_tracker/pipelinestage_list.html'
    context_object_name = 'pipeline_stages'

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'production_tracker/invoice_list.html'
    context_object_name = 'invoices'

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'production_tracker/order_form.html'
    success_url = reverse_lazy('order_list')

class IndividualCreateView(CreateView):
    model = Individual
    form_class = IndividualForm
    template_name = 'production_tracker/individual_form.html'
    success_url = reverse_lazy('individual_list')

class MeasurementCreateView(CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'production_tracker/measurement_form.html'
    success_url = reverse_lazy('measurement_list')