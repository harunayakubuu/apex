from django.urls import path
from .views import all_enquiries, enquiry_form, my_enquiries, enquiry_status_update

app_name = 'enquiries'

urlpatterns = [
    path('<int:id>/status/update/', enquiry_status_update, name = 'enquiry-status-update'),
    path('all-enquiries/', all_enquiries, name='all-enquiries'),
    path('enquiry-form/', enquiry_form, name='enquiry_form'),
    path('my-enquiries/', my_enquiries, name='my-enquiries'),
]
