import django_filters
from .models import Listing


class ListingFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    class Meta:
        model = Listing
        fields = ('category', 'listing_type', 'price')