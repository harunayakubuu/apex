from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout

from django.urls import reverse_lazy

from .forms import UserRegistrationForm, UserUpdateForm

from listings.models import Listing
from agents.models import Agent
from clients.models import Client

from pages.models import TermsAndCondition

from enquiries.models import Enquiry
from contacts.models import Contact, EmergencyContact
from django.conf import settings


User = get_user_model()


@login_required
def dashboard(request):  
    enquiries = Enquiry.objects.order_by('-created_at').filter(user_id = request.user.id)
    user_contacts = EmergencyContact.objects.filter(user__id = request.user.id)
    listings = Listing.objects.filter(listing_owner__id = request.user.id)

    context = {
        'listings': listings,
        'enquiries': enquiries,
        'user_contacts': user_contacts,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    enquiries = Enquiry.objects.order_by('-created_at').filter(user_id=request.user.id)
    user_contacts = EmergencyContact.objects.filter(user__id = request.user.id)
    emergency_contacts = EmergencyContact.objects.filter(user = request.user)

    listings = Listing.objects.order_by('created_at')
    
    context = {
        'listings': listings,
        'enquiries': enquiries,
        'emergency_contacts': emergency_contacts,
        'user_contacts': user_contacts,
    }
    return render(request, 'accounts/profile.html', context)
    

@login_required
def users_all(request):
    all_users = User.objects.all()
    context = {
        'all_users': all_users
    }
    return render(request, 'accounts/users-all.html', context)


@login_required
def user_details(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'accounts/user-details.html', context)


# Public Organisor Registration Form

def organisor_register_view(request):
    terms = TermsAndCondition.objects.filter(is_active = True)
    form = UserRegistrationForm()
    if request.method=='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_client = False
            user.is_agent = False
            user.is_organisor = True
            user.save()
            Agent.objects.create(user = user)
            Client.objects.create(user = user)
            messages.success(request, 'Registration successful.')

            message = """
            Welcome to Apex Estate Managers and Properties LTD.
            <p>
                You have registered as an agency. This gives you the priviledges of managing properties
                and agents under your agency.
            </p>
            <p>
                Currently, your is undergoing some verifications and validations. This will take some time.
                Once you satisfy our conditions, we shall approve your registration.
            </p>
            <p>
                Management,<br>
                Apex Estate Managers and Properties LTD.
            </p>
            """
            send_mail(
                subject = 'Welcome!',
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [user.email,]
            )
            return redirect('login')
        else:
            messages.error(request, 'Check and correct the error below.')
    
    context = {
        'form': form,
        'terms': terms,
    }
    return render(request, 'registration/organisor-signup.html', context)


def client_register_view(request):
    terms = TermsAndCondition.objects.filter(is_active = True)
    form = UserRegistrationForm()
    if request.method=='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_agent = False
            user.is_client = True
            user.is_organisor = False
            user.save()
            messages.success(request, 'Registration successful.')
            
            message = """
                veWelcome to Apex Estate Managers and Properties LTD.
                You have registered as client. This gives you the priviledges of managing your properties
                from your confort.
            
                Currently, your is undergoing some verifications and validations. This will take some time.
                Once you satisfy our conditions, we shall approve your registration.
          
                Management
                Apex Estate Managers and Properties LTD.
            """
            send_mail(
                subject = 'Welcome!',
                message = message,
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [user.email,]
            )
            return redirect('login')
        else:
            messages.error(request, 'Check and correct the error below.')
    context = {
        'form': form,
        'terms': terms,
    }
    return render(request, 'registration/client-signup.html', context)