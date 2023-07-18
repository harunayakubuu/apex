# Import for CSV view
import csv
import folium

import collections
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from enquiries.models import Enquiry
from pages.models import TermsAndCondition

from .filters import ListingFilter
from .forms import(
    ListingCreateForm,
    ListingUpdateForm,
    ListingSpecificationForm,
    ListingSpecificationFormset,
    ListingVideoForm,
    ListingPictureForm,
    # ListingPictureFormset,
    AssignAgentForm
)
from .models import(
    Listing,
    ListingSpecification,
    ListingVideo,
    ListingPicture,
    ListingAdditionalFeature,
    ListingNearby,
    ListingFloor,
    NearbyCategory,
)
from listings.choices import(
    state_choices, price_choices,
    bedroom_choices, type_choices,
    bathroom_choices
)



@login_required
def listing_create(request):
    terms = TermsAndCondition.objects.filter(is_active = True)
    form = ListingCreateForm()
    if request.method == 'POST':
        form = ListingCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.listing_owner = request.user.client
            obj.organization = request.user.profile
            obj.save()
            messages.success(request, 'Property saved')

            send_mail(
                subject = 'Property Submission',
                message = f'We have received a property submission ({obj.name}) from a client with this email address. Kindly note that {obj.name} shall be subjected to verifications after which it shall be published or declined depending on the outcome of the verification processess.',
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [request.user.email,]
            )
            return redirect("listings:listings-list")
    context = {
        'form': form,
        'terms': terms
    }
    return render(request, 'properties/property-add.html', context)


@login_required
def listings_list(request):
    listings = Listing.objects.order_by('-created_at')

    # # if request.user.is_organisor:
    #     agency_listings = listings.order_by('created_at')
    #     context = {
    #         'agency_listings': agency_listings
    #     }
    # if request.user.is_agent:
    #     # listings = Listing.objects.filter(organization = user.agent.organization)
    #     agency_agent_listings = listings.filter(listing_agent__user = request.user)
    #     context = {
    #         'agency_agent_listings': agency_agent_listings
    #     }
    # if request.user.is_client:
    #     client_listings = listings.filter(listing_owner__user = request.user)

    context = {
        'listings': listings
    }
    return render(request, "properties/properties-list.html", context)


@login_required
def listing_details(request, id):
    listing = Listing.objects.get(id = id)
    enquiries = Enquiry.objects.order_by('-created_at').filter(listing_id=listing.id)
    
    context = {
        'listing': listing,
        'enquiries': enquiries
    }
    
    return render(request, "properties/property-details.html", context)


def public_properties_list_view(request):
    all_listings = Listing.objects.order_by('?').filter(is_active = True, withdraw = False, approval_status='approved')
    paginator = Paginator(all_listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    states = []
    for listing in all_listings:
        states.append(listing.state)
    states_collection = collections.Counter(states)
    s = states_collection.items()

    state_set = set(states)
    states_count = len(list(state_set))

    # listing_filter = ListingFilter(request.GET, queryset=all_listings)
    # page_obj = listing_filter.qs

    context = {
        'all_listings': all_listings,
        'page_obj': page_obj,
        # 'listing_filter': listing_filter

        's': s,
        'states_count': states_count,

        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'type_choices': type_choices,
    }
    return render(request, 'properties/public-properties-list.html', context)


def public_properties_by_state(request, state):
    state = state
    state_listings = Listing.objects.order_by('-created_at').filter(is_active = True, withdraw = False, approval_status='approved').filter(state = state)
    paginator = Paginator(state_listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cities = []
    for listing in state_listings:
        cities.append(listing.city)
    cities_collection = collections.Counter(cities)
    c = cities_collection.items()     
    
    city_set = set(cities)
    cities_count = len(list(city_set))

    context = {
        'state_listings': state_listings,
        'page_obj': page_obj,

        'state': state,

        'c': c,
        'cities_count': cities_count,

        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'type_choices': type_choices,
    }
    return render(request, 'properties/public-properties-by-state.html', context)


def public_properties_by_city(request, city):
    city = city
    city_listings = Listing.objects.order_by('-created_at').filter(is_active = True, withdraw = False, approval_status='approved').filter(city = city)
    paginator = Paginator(city_listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    locations = []
    for listing in city_listings:
        locations.append(listing.location)
    locations_collection = collections.Counter(locations)
    l = locations_collection.items() 

    location_set = sorted(set(locations))
    locations_count = len(list(location_set))

    context = {
        'city_listings': city_listings,
        'page_obj': page_obj,

        'city': city,

        # 'location_set': location_set,
        'l': l,
        'locations_count': locations_count,

        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'type_choices': type_choices,
    }
    return render(request, 'properties/public-properties-by-city.html', context)


def public_properties_by_location(request, location):
    location = location
    location_listings = Listing.objects.order_by('-created_at').filter(is_active = True, withdraw = False, approval_status='approved').filter(location = location)
    paginator = Paginator(location_listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'location_listings': location_listings,
        'page_obj': page_obj,

        'location': location,

        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'type_choices': type_choices,
    }
    return render(request, 'properties/public-properties-by-location.html', context)


# Public
def public_property_detail_view(request, slug, id):
    featured_listings = Listing.objects.order_by('-created_at').filter(is_featured = True)
    listing = Listing.objects.get(
        id=id,
        slug=slug,
        is_active = True,
        withdraw = False,
        # is_verified = True
        )
    listing.view_count = listing.view_count + 1
    enquiries = Enquiry.objects.all().filter(listing_id=listing.id).count()
    listing.enquiry_count = enquiries
    listing.save()
    similar_listings = Listing.objects.filter(category = listing.category).exclude(id=id)[:6]
    # nearby_categories = set(NearbyCategory.objects.order_by('-name'))
    
    # states = []
    # for listing in all_listings:
    #     states.append(listing.state)
    # states_collection = collections.Counter(states)
    # s = states_collection.items()

    # state_set = set(states)
    # states_count = len(list(state_set))

    nearby_categories = []
    nearbys = []
    for nearby in listing.listingnearby_set.all():
        nearbys.append(nearby.category.name)
    nearby_categories_set = set(nearbys)
    # print(nearby_categories_set)
    # nearby_categories_set = set(nearby_categories)


    if listing.lat and listing.lon:
        location = [listing.lat, listing.lon]
    else:
        location = [9.2344378569, 11.9923871742]
    m = folium.Map(location=location, zoom_start=17, Tooltip="View more info.") #width=1348, height=600,
    # folium.Circle(
    #     location=location, 
    #     fill=True,
    #     stroke = True,
    #     weight = 1,
    #     radius=100,
    #     tooltip = listing.name,
    #     # popup = folium.Popup('This is a pop up', max_width = 500) # Simple popup
    #     popup = folium.Popup(listing.name,
    #         """<h5>Big House</h5><br><h6>Address of the property</h6>
    #         <img class='img-fluid' src='images/avatar/01.jpg" alt="">
    #         """,
    #         max_width = 500
    #     )
    # ).add_to(m)
    
    folium.Marker(location = location, icon=folium.Icon(color='blue')).add_to(m)
    m = m._repr_html_()
    
    context = {
        'enquiries': enquiries,
        'listing': listing,
        'similar_listings': similar_listings,
        'featured_listings': featured_listings,
        'map': m,
        'nearby_categories_set': nearby_categories_set
    }
    return render(request, 'properties/public-property-details.html', context)


def search(request):
    queryset = Listing.objects.order_by("-created_at").filter(is_active = True, withdraw = False, approval_status='approved')

    # Location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            queryset_list = queryset.filter(location__iexact=location)
        # else:
        #     queryset_list = queryset
            
    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset.filter(city__iexact=city)
        else:
            queryset_list = queryset

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset.filter(state__iexact=state)
        else:
            queryset_list = queryset

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset.filter(price__lte=price)
        else:
            queryset_list = queryset

    context = {
        'queryset_list':queryset_list,
        'queryset': queryset,

        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'bathroom_choices': bathroom_choices,
        'type_choices': type_choices,

        'values': request.GET # All field to keep values of search in a search form
    }
    return render(request, 'properties/property-search.html', context)


@login_required
def listing_update(request, id):
    instance = get_object_or_404(Listing, id=id)
    form = ListingUpdateForm(instance=instance)

    if request.method=='POST':
        form = ListingUpdateForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'Saved')
            return redirect("listings:listings-list")

    context = {
        'form': form,
        'instance': instance
    }    
    return render(request, 'properties/property-edit.html', context)


class ListingDeleteView(LoginRequiredMixin, DeleteView):
    model = Listing
    template_name = 'properties/property-delete.html'
    success_url = reverse_lazy('listings:listings-list')


def listing_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = "attachment; filename=properties.csv"

    writer = csv.writer(response)

    listings = Listing.objects.all()

    writer.writerow(['Property Name', 'Address', 'Location'])

    for listing in listings:
        writer.writerow([listing.name, listing.address, listing.location])

    return response




@login_required
def listing_video_create(request, id):
    listing = Listing.objects.get(id = id)
    form = ListingVideoForm()
    if request.method=='POST':
        form = ListingVideoForm(request.POST, request.FILES)
        if form.is_valid():

            form_istance = form.save(commit=False)
            form_istance.listing = listing
            form_istance.save()
            messages.success(request, 'Saved')
            return redirect('/properties/'+listing+'/')

    context = {
        'form': form,
        'listing': listing
    }    
    return render(request, 'properties/property-video-add.html', context)


@login_required
def listing_video_change(request, id, vid_id):
    listing = Listing.objects.get(id = id)
    instance = ListingVideo.objects.get(id = vid_id)
    form = ListingVideoForm(instance = instance)
    if request.method=='POST':
        form = ListingVideoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved')
            return redirect('listings:listings-list')

    context = {
        'form': form,
        # 'listing': listing
    }    
    return render(request, 'properties/property-video-change.html', context)


@login_required
def listing_picture_add(request, id):
    listing = Listing.objects.get(id = id)
    ListingPictureFormset = inlineformset_factory(Listing, ListingPicture, fields = ('name', 'picture', 'is_feature'), extra = 6)
    # listing = Listing.objects.get(id = id)
    formset = ListingPictureFormset(instance = listing)
    if request.method=='POST':
        formset = ListingPictureFormset(request.POST, request.FILES, instance = listing)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Saved')
            # return redirect('listings:listing-details')
            # return redirect('listings:listing-details')

    context = {
        'formset': formset,
        # 'listing': listing
    }    
    return render(request, 'properties/pictures/property-pictures-add.html', context)


@login_required
def listing_floor_add(request, id):
    listing = Listing.objects.get(id = id)
    ListingFloorFormset = inlineformset_factory(
        Listing,
        ListingFloor,
        fields = ['floor', 'number_of_rooms', 'rest_rooms', 'parlor', 'store', 'floor_plan'],
        extra = 2,
        max_num = 10,
        min_num = 1
        )
    # listing = Listing.objects.get(id = id)
    formset = ListingFloorFormset(instance = listing)
    if request.method=='POST':
        formset = ListingFloorFormset(request.POST, request.FILES, instance = listing)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Saved')
            return redirect('listings:listings-list')
        else:
            print("Errors")
    context = {
        'formset': formset,
        'listing': listing
    }
    return render(request, 'properties/floors/property-floors-add.html', context)


@login_required
def listing_specification_add(request, id):
    listing = Listing.objects.get(id = id)
    ListingSpecsFormset = inlineformset_factory(Listing, ListingSpecification, fields = ('attribute', 'value'), extra = 6)
    # listing = Listing.objects.get(id = id)
    formset = ListingSpecsFormset(instance = listing)
    if request.method=='POST':
        formset = ListingSpecsFormset(request.POST, instance = listing)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Saved')
            return redirect('listings:listings-list')
    context = {
        'formset': formset,
        'listing': listing

    }
    return render(request, 'properties/specs/property-specs-add.html', context)


@login_required
def listing_additional_features_add(request, id):
    listing = Listing.objects.get(id = id)
    ListingAdditionalFeaturesFormset = inlineformset_factory(Listing, ListingAdditionalFeature, fields = ('feature',), extra = 1, max_num=1)
    # listing = Listing.objects.get(id = id)
    formset = ListingAdditionalFeaturesFormset(instance = listing)
    if request.method=='POST':
        formset = ListingAdditionalFeaturesFormset(request.POST, instance = listing)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Saved')
            return redirect('listings:listings-list')
    context = {
        'formset': formset,
        'listing': listing

    }
    return render(request, 'properties/additional-features/property-additional-features-add.html', context)


@login_required
def listing_nearby_add(request, id):
    listing = Listing.objects.get(id = id)
    ListingNearbyFormset = inlineformset_factory(
        Listing,
        ListingNearby,
        fields = ('category', 'name', 'location', 'approximate_distance'),
        # extra = 1,
        # max_num=1
        )
    # listing = Listing.objects.get(id = id)
    formset = ListingNearbyFormset(instance = listing)
    if request.method=='POST':
        formset = ListingNearbyFormset(request.POST, instance = listing)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Saved')
            return redirect('listings:listings-list')
    context = {
        'formset': formset,
        'listing': listing

    }
    return render(request, 'properties/nearbys/property-nearby-add.html', context)


@login_required
def assign_agent(request, id):
    listing = Listing.objects.get(id = id)
    form = AssignAgentForm()
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'listing': listing
    }
    return render(request, 'properties/assign-agent.html', context)