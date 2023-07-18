from pyexpat import model
from import_export import resources
from django.contrib import admin
from .models import (
    Category,
    Listing,

    ListingPicture,
    ListingVideo,

    ListingFeature,
    ListingAdditionalFeature,

    ListingAttribute,
    ListingSpecification,
    
    ListingType,

    ListingFloor,

    ListingNearby,
    NearbyCategory   
)

from import_export import resources
from import_export.admin import ExportActionMixin

    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ListingFeatureAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(ListingFeature, ListingFeatureAdmin)


class NearbyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(NearbyCategory, NearbyCategoryAdmin)



class ListingAttributeInline(admin.TabularInline):
    model = ListingAttribute


class ListingTypeAdmin(admin.ModelAdmin):
    inlines = [
        ListingAttributeInline
    ]
    list_display = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(ListingType, ListingTypeAdmin)


class ListingSpecificationInline(admin.TabularInline):
    model = ListingSpecification
    extra = 1


class ListingPictureInline(admin.TabularInline):
    model = ListingPicture
    extra = 1


class ListingVideoInline(admin.TabularInline):
    model = ListingVideo
    extra = 1


class ListingAdditionalFeatureInline(admin.TabularInline):
    model = ListingAdditionalFeature
    extra = 1


class ListingFloorInline(admin.TabularInline):
    model = ListingFloor
    extra = 1
    

class ListingNearbyInline(admin.StackedInline):
    model = ListingNearby
    extra = 1


class ListingResource(resources.ModelResource):
    model = Listing
    fields = ('id', 'name', 'description', 'address')
    # export_order = ('id', 'location', 'listing_owner')


class ListingAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = ListingResource
    inlines = [
        ListingSpecificationInline,
        ListingPictureInline,
        ListingVideoInline,
        ListingAdditionalFeatureInline,
        ListingFloorInline,
        ListingNearbyInline
    ]
    list_display = ('name', 'description', 'address', 'is_locked')
    # readonly_fields = ['listing_owner']
    list_filter = ('is_active', 'is_locked', 'created_at', 'updated_at')
    raw_id_fields = ['listing_agent', 'listing_owner']
    list_per_page = 20
    

admin.site.register(Listing, ListingAdmin)