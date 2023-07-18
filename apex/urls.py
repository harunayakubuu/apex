from django.contrib import admin
from django.conf.urls import handler404, handler500
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from accounts.views import organisor_register_view, client_register_view


urlpatterns = [
    path('account/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path('', include('pages.urls', namespace = 'pages')),
    path('agencies/', include('agencies.urls', namespace = 'agencies')),
    path('agents/', include('agents.urls', namespace = 'agents')),
    path('clients/', include('clients.urls', namespace = 'clients')),
    path('blog/', include('blog.urls', namespace = 'blog')),
    path('contacts/', include('contacts.urls', namespace = 'contacts')),
    path('enquiries/', include('enquiries.urls', namespace = 'enquiries')),
    path('faqs/', include('faqs.urls', namespace = 'faqs')),
    path('invoices/', include('invoices.urls', namespace = 'invoices')),
    path('properties/', include('listings.urls', namespace = 'listings')),
    path('sales/', include('sales.urls', namespace = 'sales')),

    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('signup/client/', client_register_view, name = 'client-signup'),
    path('signup/agency/', organisor_register_view, name = 'organisor-signup'),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done',),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm',),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete',),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler404='apex.views.page_not_found_view'
handler500='apex.views.server_error_view'