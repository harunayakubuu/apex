from django.urls import path
from . import views


app_name = "clients"


urlpatterns = [
    path('', views.client_list, name = 'clients-list'),
    path('client/create/form/', views.client_create, name = 'client-create'),
    path('client/edit/form/', views.client_update, name = 'client-update'),
    path('client/user/<int:id>/details/', views.admin_client_user_details, name = 'admin-client-user-details'),
    path('client/user/<int:id>/update/form/', views.admin_client_user_update, name = 'admin-client-user-update'),
    path('client/user/<int:pk>/delete/', views.AdminClientUserDeleteView.as_view(), name = 'admin-client-user-delete'),
]