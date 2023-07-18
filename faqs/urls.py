from django.urls import path
from .views import faqs, all_faqs, faqs_create, faqs_delete, faqs_edit

app_name = 'faqs'

urlpatterns = [
    path('', faqs, name = 'faqs'),
    path('all/', all_faqs, name = 'all-faqs'),
    path('create/', faqs_create, name = 'faqs-create'),
    path('faq/<int:id>/update/', faqs_edit, name = 'faqs-edit'),
    path('<int:id>/delete/', faqs_delete, name = 'faqs-delete'),
]