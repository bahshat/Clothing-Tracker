from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import Order, OrderStage, Individual, Measurement, VendorRole, Vendor, PipelineStage, Invoice
from .forms import OrderStageUpdateForm, OrderForm, IndividualForm, MeasurementForm, OrderStageCreateForm
from datetime import date
from django.contrib.auth.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginView(LoginView):
    template_name = 'production_tracker/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        refresh = RefreshToken.for_user(user)
        self.request.session['access_token'] = str(refresh.access_token)
        self.request.session['refresh_token'] = str(refresh)
        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'production_tracker/dashboard.html'

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'production_tracker/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'production_tracker/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stage_update_form'] = OrderStageUpdateForm()
        context['stage_create_form'] = OrderStageCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = OrderStageCreateForm(request.POST)
        if form.is_valid():
            order_stage = form.save(commit=False)
            order_stage.order = self.object
            order_stage.save()
            return redirect('order_detail', pk=self.object.pk)
        else:
            context = self.get_context_data(**kwargs)
            context['stage_create_form'] = form # Pass the form with errors back to the template
            return self.render_to_response(context)

class UpdateOrderStageView(LoginRequiredMixin, View):
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

class IndividualListView(LoginRequiredMixin, ListView):
    model = Individual
    template_name = 'production_tracker/individual_list.html'
    context_object_name = 'individuals'

class MeasurementListView(LoginRequiredMixin, ListView):
    model = Measurement
    template_name = 'production_tracker/measurement_list.html'
    context_object_name = 'measurements'

class VendorRoleListView(LoginRequiredMixin, ListView):
    model = VendorRole
    template_name = 'production_tracker/vendorrole_list.html'
    context_object_name = 'vendor_roles'

class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'production_tracker/vendor_list.html'
    context_object_name = 'vendors'

class PipelineStageListView(LoginRequiredMixin, ListView):
    model = PipelineStage
    template_name = 'production_tracker/pipelinestage_list.html'
    context_object_name = 'pipeline_stages'

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'production_tracker/invoice_list.html'
    context_object_name = 'invoices'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'production_tracker/order_form.html'
    success_url = reverse_lazy('order_list')

class IndividualCreateView(LoginRequiredMixin, CreateView):
    model = Individual
    form_class = IndividualForm
    template_name = 'production_tracker/individual_form.html'
    success_url = reverse_lazy('individual_list')

class MeasurementCreateView(LoginRequiredMixin, CreateView):
    model = Measurement
    form_class = MeasurementForm
    template_name = 'production_tracker/measurement_form.html'
    success_url = reverse_lazy('measurement_list')
