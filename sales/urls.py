from django.urls import path
from .views import SalesListView, SalesDetailView, customer_create, position_create, sale_create

app_name = 'sales'

urlpatterns = [
    path('position/add/', position_create, name = 'position-create'),
    path('sale/add/', sale_create, name = 'sale-create'),
    path('customer/add/', customer_create, name = 'customer-create'),
    path('list/', SalesListView.as_view(), name = 'sales-list'),
    path('<int:pk>/details/', SalesDetailView.as_view(), name = 'sales-detail'),
]