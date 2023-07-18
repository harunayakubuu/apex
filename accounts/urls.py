from django.urls import path
from .views import dashboard, profile, users_all, user_details

app_name = "accounts"

urlpatterns = [
    path('dashboard/', dashboard, name = 'dashboard'),
    path('profile/', profile, name = 'profile'),
    path('users/all/', users_all, name = 'all-users'),
    path('users/user/<int:id>/', user_details, name = 'user-details'),
]