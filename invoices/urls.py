from django.urls import path
from .views import SaleListView, render_pdf_view, sales_render_pdf


app_name = "invoices"


urlpatterns = [
    path('sales/', SaleListView.as_view(), name = 'sales_list'),
    path('', render_pdf_view, name = 'invoices'),
    path('sales/<pk>/pdf/', sales_render_pdf, name = 'sale-pdf'),
]