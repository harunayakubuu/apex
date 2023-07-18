from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Position, Sale
from .forms import PositionForm, SaleForm, SaleSearchForm

from clients.models import Customer
from clients.forms import CustomerForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def position_create(request):
    if request.user.is_superuser:
        form = PositionForm()
        if request.method=='POST':
            form = PositionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Position has been created")
                return redirect('sales:sale-create')
        context = {
            'form': form
        }
    else:
        messages.success(request, "You dont have permission to access this page.")
        return redirect('accounts:dashboard')
    return render(request, 'sales/position-create.html', context)


@login_required
def sale_create(request):
    if request.user.is_superuser:
        form = SaleForm()
        if request.method=='POST':
            form = SaleForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Sale created')
                return redirect('sales:sales-list')
        context = {
            'form': form
        }
    else:
        messages.success(request, "You dont have permission to access this page.")
        return redirect('accounts:dashboard')
    return render(request, 'sales/sale-create.html', context)


@login_required
def customer_create(request):
    form = CustomerForm()
    if request.method=='POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Added created')
            return redirect('sales:sale-create')
    context = {
        'form': form
    }
    return render(request, 'sales/buyer-add.html', context)


class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sales-list.html'


class SalesDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sales-detail.html'