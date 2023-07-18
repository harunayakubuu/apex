from django.urls import path
from .views import(
    admin_organisor_user_create,
    AdminOrganisorUserDeleteView,
    admin_organisor_user_details,
    admin_organisor_users_list,
    admin_organisor_user_update,

    organisor_create,
    organisor_details,
    organisor_list,
    organisor_update,

    agencies_list,
    agency_create,
    agency_detail,
    agency_update,
    admin_agency_update,
    AgencyDeleteView,
    public_agency_list, 
    public_agency_details,
)

app_name = 'agencies'

urlpatterns = [
    
    path('organisor/update/', organisor_update, name = 'organisor-update'),
    path('organisor/create/', organisor_create, name = 'organisor-create'),
    path('organisors/list/', organisor_list, name = 'organisors-list'),
    
    path('organisor/user/create/', admin_organisor_user_create, name = 'admin-organisor-user-create'),
    path('organisor/users/list/', admin_organisor_users_list, name = 'admin-organisor-users-list'),
    
    path('list/', agencies_list, name = 'agencies-list'),
    path('create/', agency_create, name = 'agency-create'),
    path('p/list/', public_agency_list, name = 'public-agency-list'),
    path('p/<str:slug>/', public_agency_details, name = 'public-agency-details'),
    
    path('organisor/user/<int:id>/details/', admin_organisor_user_details, name = 'admin-organisor-user-details'),
    path('organisor/user/<int:id>/update/', admin_organisor_user_update, name = 'admin-organisor-user-update'),
    path('organisor/user/<int:pk>/delete/', AdminOrganisorUserDeleteView.as_view(), name = 'admin-organisor-user-delete'),
    
    path('<int:pk>/delete/', AgencyDeleteView.as_view(), name = 'agency-delete'),
    
    path('<str:slug>/', agency_detail, name = 'agency-details'),
    path('<str:slug>/update/', agency_update, name = 'agency-update'),
    path('admin/agency/<str:slug>/update/', admin_agency_update, name = 'admin-agency-update'),
    path('<int:id>/organisor/details/', organisor_details, name = 'organisor-details'),
]