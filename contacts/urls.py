from django.urls import path
from . import views 

app_name = 'contacts'

urlpatterns = [
    path('contact/form/', views.contact_form, name = 'contact-form'),
    path('contact/messages/', views.contact_messages, name = 'contact-messages'),
    path('contact/message/<int:id>/details/', views.contact_message_detail, name = 'contact-message-details'),
    path('contact/message/<int:id>/update/', views.contact_message_update, name = 'contact-message-update'),
    path('contact/message/<int:pk>/delete/', views.ContactMessageDeleteView.as_view(), name = 'contact-message-delete'),
    # path('contact/message/<int:id>/delete/', views.contact_message_delete, name = 'contact-message-delete'),

    path('emergency-contacts/', views.emergency_contacts, name = 'emergency-contacts'),
    path('emergency-contact/create/', views.emergency_contact_create, name = 'emergency-contact-create'),
    path('emergency-contact/<int:id>/edit/', views.emergency_contact_edit, name = 'emergency-contact-edit'),
    path('emergency-contact/<int:id>/delete/', views.emergency_contact_delete, name = 'emergency-contact-delete'),
    
    path('offices/', views.offices, name = 'offices'),
]