from django.urls import path
from .views import(
  listing_create,
  listings_list,
  search,
  # listing_hx_details,
  listing_update,
  listing_details,
  ListingDeleteView,
  # listing_spec_hx_update,
  
  public_properties_list_view,
  public_properties_by_state,
  public_properties_by_city,
  public_properties_by_location,
  public_property_detail_view,

  listing_csv,

  listing_video_create,
  listing_video_change,

  listing_picture_add,
  # listing_picture_update,
  # picture_form,

  listing_floor_add,
  # listing_floor_update,

  # listing_attribute_add,
  # listing_attribute_update,

  listing_specification_add,
  # listing_specification_update,

  listing_additional_features_add,
  # listing_additional_features_update,

  listing_nearby_add,
  # listing_nearby_update,
  assign_agent,
)

app_name  = 'listings'


urlpatterns = [
    path('all/', public_properties_list_view, name = 'public-properties-list'),
    path('state/<str:state>/', public_properties_by_state, name = 'public-properties-by-state'),
    path('city/<str:city>/', public_properties_by_city, name = 'public-properties-by-city'),
    path('location/<str:location>/', public_properties_by_location, name = 'public-properties-by-location'),
    path('search/list/', search, name='search'),

    path('property/add/', listing_create, name='listing-add'),
    path('property/csv/', listing_csv, name='listing-csv'),
    path('list/', listings_list, name='listings-list'),

    path('property/<str:id>/edit/', listing_update, name='listing-edit'),
    path('property/<str:pk>/delete/', ListingDeleteView.as_view(), name='listing-delete'),

    path('<str:slug>/<str:id>/', public_property_detail_view, name = 'public-property-details'),

    path('<str:id>/', listing_details, name='listing-details'),

    path('<str:id>/video/add/', listing_video_create, name='listing-video-add'),
    path('<str:id>/video/<int:vid_id>/change/', listing_video_change, name='listing-video-change'),

    path('<str:id>/pictures/add/', listing_picture_add, name='listing-picture-add'),
    path('<str:id>/specifications/add/', listing_specification_add, name='listing-specs-add'),
    path('<str:id>/additional-features/add/', listing_additional_features_add, name='listing-additional-features-add'),
    path('<str:id>/nearby/add/', listing_nearby_add, name='listing-nearby-add'),
    path('<str:id>/floors/add/', listing_floor_add, name='listing-floor-add'),
    
    path('<str:id>/assign-agent/', assign_agent, name='assign-agent'),
  ]

   # path('hx/<str:id>/', listing_hx_details, name='listing-hx-details'),

    # path('<str:parent_id>/hx/specifications/<int:id>/', listing_spec_hx_update, name='hx-spec-detail'),
    # path('<str:parent_id>/hx/specifications/create/', listing_spec_hx_update, name='spec-create'),