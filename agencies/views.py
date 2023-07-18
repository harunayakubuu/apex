import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from django.core.paginator import Paginator

from listings.models import Listing

from .models import Agency, Organisor
from .forms import (
    AdminOrganisorUserCreateForm, AdminOrganisorUserUpdateForm, 
    OrganisorCreateForm, OrganisorUpdateForm, 
    AgencyCreateForm, AgencyUpdateForm, AdminAgencyUpdateForm
)
from accounts.forms import UserUpdateForm

from agents.models import Agent
from clients.models import Client

import folium

User = get_user_model()


# User Organisor Creation by the admin
@login_required
def admin_organisor_user_create(request):
    if request.user.is_superuser or request.user.is_staff:
        form = AdminOrganisorUserCreateForm()
        if request.method == 'POST':
            form = AdminOrganisorUserCreateForm(request.POST, request.FILES or None)
            if form.is_valid():
                user = form.save(commit = False)
                user.is_client = False
                user.is_agent = False
                user.is_organisor = True
                user.set_password(f'{random.randint(0, 1000000000)}')
                user.save()
                Agent.objects.create(user=user)
                Client.objects.create(user=user)
                send_mail(
                    subject = "Invitation to join Apex Extate Managers and Properties Platform as an Independent Agency.",
                    message = "You have been added as an independent agency. Please reset your password to be able to log in to start working.",
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [user.email,]
                )
                messages.success(request, 'Agency manager created successfully.')
                return redirect('agencies:admin-organisor-users-list')
            else:
                messages.error(request, 'Check the form and try again.') 
        context = {
            'form': form,
        }
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard')
    return render(request, 'agencies/organisors/admin-organisor-user-create-form.html', context)


# This returns the list of all organisors to the super admin
@login_required
def admin_organisor_users_list(request):
    if request.user.is_superuser or request.user.is_staff:
        organisors = User.objects.order_by('-date_joined').filter(is_organisor=True)
        context = {
            'organisors': organisors
        }
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard')
    return render(request, 'agencies/organisors/admin-organisor-users-list.html', context)


# This returns the details of an organisor to the super admin
@login_required
def admin_organisor_user_update(request, id):
    user = get_object_or_404(User, id = id)
    if request.user.is_superuser:
        form = AdminOrganisorUserUpdateForm(instance=user)
        if request.method == 'POST':
            form = AdminOrganisorUserUpdateForm(request.POST, request.FILES or None, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes saved.')
                return redirect('agencies:admin-organisor-users-list')
            else:
                messages.error(request, 'Check the form and try again.') 
        context = {
            'form': form,
        }
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard')
    return render(request, 'agencies/organisors/admin-organisor-user-update-form.html', context)


@login_required
def admin_organisor_user_details(request, id):
    organisor = get_object_or_404(User, id = id)
    context = {
        'organisor': organisor
    }
    return render(request, 'agencies/organisors/admin-organisor-user-details.html', context)


class AdminOrganisorUserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'agencies/organisors/admin-organisor-user-delete.html'
    success_url = reverse_lazy('agencies:admin-organisor-users-list')


@login_required
def organisor_create(request):
    user_obj = request.user

    user_form = UserUpdateForm(instance=request.user)
    organisor_form = OrganisorCreateForm()

    if request.method == 'POST':

        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        organisor_form = OrganisorCreateForm(request.POST, request.FILES)

        if user_form.is_valid() and organisor_form.is_valid():
            user_form.save()
            organisor_obj = organisor_form.save(commit = False)
            organisor_obj.user = user_obj
            organisor_obj.save()
            
            messages.success(request, 'Profile Updated.')
            return redirect('accounts:profile')
        else:
           messages.error(request, 'Check the form and try again.') 
    context = {
        'user_form': user_form,
        'organisor_form': organisor_form
    }
    return render(request, 'agencies/organisors/organisor-create-form.html', context)


def organisor_update(request):
    organisor_obj  = request.user.organisor

    user_form = UserUpdateForm(instance=request.user)
    organisor_update_form = OrganisorUpdateForm(instance = organisor_obj)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        organisor_update_form = OrganisorUpdateForm(request.POST, request.FILES or None, instance = organisor_obj)
        if organisor_update_form.is_valid() and user_form.is_valid():
            user_form.save()
            organisor_update_form.save()
            messages.success(request, 'Changes Saved.')
            return redirect('accounts:profile')
        else:
           messages.error(request, 'Check the form and try again.') 
    context = {
        'user_form': user_form,
        'organisor_update_form': organisor_update_form,
        'organisor': organisor_obj
    }
    return render(request, 'agencies/organisors/organisor-user-update-form.html', context)


@login_required
def organisor_list(request):
    organisor_list = Organisor.objects.order_by('-created_date')
    context = {
        'organisor_list': organisor_list
    }
    return render(request, 'agencies/organisors/organisor-user-list.html', context)


@login_required
def organisor_details(request, id):
    organisor = Organisor.objects.get(id=id)
    context = {
        'organisor':organisor,
    }
    return render(request, 'agencies/organisors/organisor-user-details.html', context)


@login_required
def agency_create(request):
    form = AgencyCreateForm()
    if request.method == 'POST':
        form = AgencyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.profile = request.user.profile
            form_obj.save()
            messages.success(request, "Agency Created Successfully.")

            message = """
            <p>
                Registration of f'{form_obj.name}' is successful.<br>
                Properties can now be listed under this agency.
            </p>
            <p>
                Management,<br>
                Apex Estate Managers and Properties LTD.
            </p>
            """
            send_mail(
                subject = 'Agency Registration',
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [request.user.email, form_obj.email]
            )

    context = {
        'form': form
    }
    return render(request, 'agencies/agencies/agency-create.html', context)


@login_required
def agency_detail(request, slug):
    agency = get_object_or_404(Agency, slug = slug)
    context = {
        'agency': agency,
    }
    return render(request, 'agencies/agencies/agency-details.html', context)


@login_required
def agency_update(request, slug):
    agency = get_object_or_404(Agency, slug = slug)
    form = AgencyUpdateForm(instance = agency)
    if request.method == 'POST':
        form = AgencyUpdateForm(request.POST, request.FILES, instance = agency)
        if form.is_valid():
            form.save()
            messages.success(request, "Agency Updated Successfully.")
    context = {
        'form': form
    }
    return render(request, 'agencies/agencies/agency-update.html', context)


@login_required
def admin_agency_update(request, slug):
    agency = get_object_or_404(Agency, slug = slug)
    form = AdminAgencyUpdateForm(instance = agency)
    if request.method == 'POST':
        form = AdminAgencyUpdateForm(request.POST, request.FILES, instance = agency)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes saved.")
    context = {
        'form': form,
        'agency': agency
    }
    return render(request, 'agencies/agencies/admin-agency-update-form.html', context)


class AgencyDeleteView(LoginRequiredMixin, DeleteView):
    model = Agency
    template_name = 'agencies/agencies/agency-delete.html'
    success_url = reverse_lazy('agencies:agencies-list')


@login_required
def agencies_list(request):
    agencies = Agency.objects.all()
    context = {
        "agencies": agencies
    }
    return render(request, 'agencies/agencies/agencies-list.html', context)
    

def public_agency_list(request):
    agencies = Agency.objects.order_by('created_date').filter(status = 'APPROVED')
    paginator = Paginator(agencies, 20) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    agencies_obj = paginator.get_page(page_number)
    agency_listings_count = 0
    for agency in agencies_obj:
        agency_listings_count = Listing.objects.filter(organization=agency.profile).count()

    context = {
        'agencies_obj': agencies_obj,
        'agency_listings_count': agency_listings_count
    }
    return render(request, 'agencies/agencies/public-agency-list.html', context)


def public_agency_details(request, slug):
    agency = get_object_or_404(Agency, slug = slug)
    agency_listings = Listing.objects.filter(organization=agency.profile)
    agency_agents = Agent.objects.filter(organization=agency.profile)

    # if agency.location_lat and agency.location_lon:
    #     location = [agency.location_lat, agency.location_lon]

    #     m = folium.Map(location = location, zoom_start=17, Tooltip="View more info.")
    #     folium.Marker(location = location, icon=folium.Icon(color='blue')).add_to(m)
    #     m = m._repr_html_()

    #     context = {
    #         'agency': agency,
    #         'map': m,
    #     }
    # else:
    context = {
        'agency': agency,
        'agency_listings': agency_listings,
        'agency_agents': agency_agents
    }
    return render(request, 'agencies/agencies/public-agency-details.html', context)