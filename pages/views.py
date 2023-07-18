from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TermsAndCondition, PrivacyPolicy
from .forms import (
    PrivacyPolicyForm, PrivacyPolicyEditForm,
    TermsAndConditionForm, TermsAndConditionEditForm,
    ServiceForm, ServiceEditForm#, AboutUsForm
)
from django.contrib import messages
# from django.contrib.auth import get_user_model
from listings.models import Listing
from agents.models import Agent
from blog.models import Post
from faqs.models import Testimonial
from accounts.models import Team
from .models import Service# PrivacyPolicy, TermsAndCondition

from listings.choices import state_choices, price_choices, bedroom_choices, type_choices, bathroom_choices

import folium
from folium.plugins import MarkerCluster

import collections

# User = get_user_model()


def index(request):
    active_listings = Listing.objects.order_by('-created_at').filter(is_active=True, withdraw = False, approval_status='approved')
    featured_listings = Listing.objects.order_by('-created_at').filter(is_active=True, is_featured=True, withdraw = False, approval_status='approved')[:6]
    offers = Listing.objects.order_by('-created_at').filter(is_active=True, withdraw = False, approval_status='approved', discount_available = True)
    latest_posts = Post.objects.order_by('-created_at').filter(is_active=True)[:3]
    featured_agents = Agent.objects.order_by('-user').filter(user__is_active = True).filter(user__is_organisor = False)[:3]

    m = folium.Map(location=[9.616998220327963, 8.025512695312502], zoom_start=7) #width=1348, height=600,   

    mCluster = MarkerCluster().add_to(m)

    locations = []
    for listing in active_listings:
        locations.append(listing.location)
    location_set = set(locations)
    locations_count = len(list(location_set))


    states = []
    for listing in active_listings:
        states.append(listing.state)
    states_collection = collections.Counter(states)
    s = states_collection.items()

    state_set = set(states)
    states_count = len(list(state_set))

    # map_data = []

    for listing in active_listings:
        if listing.lon and listing.lat: 
            folium.Marker([listing.lat, listing.lon], icon=folium.Icon(color='blue')).add_to(mCluster) 

            # folium.Circle(
            #     location=[data[0], data[1]], 
            #     fill=True,
            #     stroke = True,
            #     weight = 1,
            #     radius=20000,
            #     tooltip = data[2],
            #     # popup = folium.Popup('This is a pop up', max_width = 500) # Simple popup
            #     popup = folium.Popup(data[2],
            #         """<h5>data[2]</h5>
            #         <img class='img-fluid' src='images/avatar/01.jpg" alt="">
            #         """,
            #         max_width = 500
            #     )
            # ).add_to(m),
        
    folium.LayerControl().add_to(m)
    m = m._repr_html_()

    agents_count = Agent.objects.filter(user__is_active = True, is_active = True).filter(user__is_organisor = False).count()
    listing_sale_count = Listing.objects.filter(is_active = True, withdraw = False, status = 'sale').count()
    listing_rent_count = Listing.objects.filter(is_active = True, withdraw = False, status = 'rent').count()
    
    context = {
        'locations_count': locations_count,
        'location_set': location_set,

        # 'state_set': state_set,
        'states_count': states_count,
        's': s,

        'active_listings': active_listings,
        'featured_listings': featured_listings,
        'offers': offers,

        'featured_agents': featured_agents,

        'map':m,
        'latest_posts': latest_posts,

        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'bathroom_choices': bathroom_choices,
        'type_choices': type_choices,

        'agents_count': agents_count,
        'listing_sale_count': listing_sale_count,
        'listing_rent_count': listing_rent_count,
    }
    return render(request, 'pages/index.html', context)


def about(request):
    services = Service.objects.order_by("-created_at").filter(is_active = True)
    active_listings = Listing.objects.order_by('-created_at').filter(is_active=True, withdraw = False, approval_status='approved')
    locations = []
    for listing in active_listings:
        locations.append(listing.location)

    location_set = set(locations)
    locations_count = len(list(location_set))

    testimonials = Testimonial.objects.order_by('-created_at').filter(is_active=True)[:10]
    # listing_agents= Agent.objects.all()
    # # team_members = User.objects.filter(is_team_member=True)
    # # mvp_agent = Agent.objects.filter(is_mvp = True)
    team_members = Team.objects.filter(user__is_active=True)
    agents_count = Agent.objects.filter(user__is_active = True, is_active = True).filter(user__is_organisor = False).count()
    listing_sale_count = Listing.objects.filter(is_active = True, withdraw = False, status = 'sale').count()
    listing_rent_count = Listing.objects.filter(is_active = True, withdraw = False, status = 'rent').count()
    context = {
        'services': services,
        'locations_count': locations_count,
        'testimonials': testimonials,
        # 'listing_agents': listing_agents,
        # 'mvp_agent':mvp_agent
        'agents_count': agents_count,
        # 'listings': listings,
        'team_members': team_members,
        'listing_sale_count': listing_sale_count,
        'listing_rent_count': listing_rent_count
    }
    return render(request, 'pages/about-us.html', context)


def privacy_policy(request):
    policies = PrivacyPolicy.objects.all()
    context = {
        'policies': policies
    }
    return render(request, 'pages/privacy-policy.html', context)


@login_required
def policies(request):
    policies = PrivacyPolicy.objects.all()
    context = {
        'policies': policies
    }
    return render(request, 'pages/policies.html', context)


@login_required
def policy_create(request):
    form = PrivacyPolicyForm()
    if request.method == 'POST':
        form = PrivacyPolicyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('pages:policies')
    context = {
        'form': form
    }
    return render(request, 'pages/privacy-policy-create-form.html', context)


@login_required
def policy_edit(request, id):
    instance = PrivacyPolicy.objects.get(id = id)
    form = PrivacyPolicyEditForm(instance=instance)
    if request.method == 'POST':
        form = PrivacyPolicyEditForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfull.')
            return redirect('pages:policies')
        else:
             messages.error(request, 'Invalid form')
    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'pages/privacy-policy-edit-form.html', context)


def signup(request):
    context = {
        
    }
    return render(request, 'registration/register.html', context)


def t_and_c(request):
    terms = TermsAndCondition.objects.all()
    context = {
        'terms': terms
    }
    return render(request, 'pages/terms-and-conditions.html', context)


@login_required
def terms(request):
    terms = TermsAndCondition.objects.filter(is_active=True)
    context = {
        'terms': terms
    }
    return render(request, 'pages/terms.html', context)


@login_required
def terms_create(request):
    form = TermsAndConditionForm()
    if request.method == 'POST':
        form = TermsAndConditionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('pages:terms')
    context = {
        'form': form
    }
    return render(request, 'pages/terms-create-form.html', context)


@login_required
def terms_edit(request, id):
    instance = TermsAndCondition.objects.get(id = id)
    form = TermsAndConditionEditForm(instance=instance)
    if request.method == 'POST':
        form = TermsAndConditionEditForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfull.')
            return redirect('pages:terms')
        else:
             messages.error(request, 'Invalid form')
    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'pages/terms-edit-form.html', context)


@login_required
def services_list(request):
    services = Service.objects.order_by("-created_at")
    context = {
        'services': services
    }
    return render(request, 'pages/services-list.html', context)


@login_required
def service_create(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saved.')
            return redirect('pages:services-list')
    context = {
        'form': form
    }
    return render(request, 'pages/service-create-form.html', context)


@login_required
def service_edit(request, id):
    instance = Service.objects.get(id = id)
    form = ServiceEditForm(instance=instance)
    if request.method == 'POST':
        form = ServiceEditForm(request.POST, instance = instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfull.')
            return redirect('pages:services-list')
        else:
             messages.error(request, 'Invalid form')
    context = {
        'form': form,
        'instance': instance
    }
    return render(request, 'pages/service-edit-form.html', context)