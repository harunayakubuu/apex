import uuid
import random
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import Profile

from agents.models import Agent
from clients.models import Client

from mptt.models import MPTTModel, TreeForeignKey

from ckeditor.fields import RichTextField

from .choices import STATE_CHOICES, state_choices
from .validators import validate_picture_size, validate_picture_dimension, validate_video_size, validate_floor_design_size

# The best way to get the user model in a model file
User = settings.AUTH_USER_MODEL

# the best way to get the user model elsewhere outside of the model file
# from django.contrib.auth import get_user_model
# User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True, verbose_name ='Category Name')
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField("Active", default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Listing(models.Model):
    id              = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    listing_owner   = models.ForeignKey(Client, on_delete = models.CASCADE, related_name="owner")
    organization    = models.ForeignKey(Profile, blank = True, null = True, on_delete=models.CASCADE)
    listing_agent   = models.ForeignKey(Agent, on_delete = models.SET_NULL, null = True, blank = True, related_name="agent")
    category        = models.ForeignKey(Category, on_delete = models.RESTRICT)
    listing_type    = models.ForeignKey('ListingType', on_delete = models.DO_NOTHING)
    name            = models.CharField(verbose_name='Property name', max_length = 255)
    price           = models.PositiveIntegerField(blank=True, null=True, help_text = "in Nigerian naira #")
    
    PRICE_STATUS_CHOICES = (
        ('fixed', 'Fixed Price'),
        ('negotiable', 'Price Negoiable')
    )

    price_status    = models.CharField(max_length = 255, choices = PRICE_STATUS_CHOICES, blank = True, null = True, default = 'negotiable')

    STATUS_CHOICES  = (
        ('rent', 'For Rent'),
        ('sale', 'For Sale')
    )
    status          = models.CharField(max_length = 10, choices = STATUS_CHOICES, default='sale')
    # description     = RichTextField()
    description     = models.TextField(blank=True, null=True)

    length           = models.PositiveIntegerField('Length of Plot', help_text = "Length of plot in feet. E.g 50")
    breadth           = models.PositiveIntegerField('Breadth of Plot', help_text = "Breadth of plot in feet. E.g 50")
    
    address         = models.CharField(max_length = 255, verbose_name='Property address')
    
    slug            = models.SlugField(unique=True, blank = True, null = True)
    location        = models.CharField(max_length = 255, verbose_name = 'Property Location')

    lat             = models.FloatField(blank = True, null = True)
    lon             = models.FloatField(blank = True, null = True)

    city            = models.CharField(max_length = 255, verbose_name = 'City/Town')
    state           = models.CharField(max_length = 20, verbose_name = 'State', choices=STATE_CHOICES)
    
    encumbrances    = models.BooleanField("Is there any encumbrances on this property?", help_text = "Check the box if this property is under any encumbrances. Eg. Bank loan.", default = False)
    encumbrance_description = models.CharField(max_length = 255, verbose_name='Encumbrance description', null = True, blank = True)
    
    APPROVAL_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapproved', 'Disapproved'),
    )
    approval_status = models.CharField(max_length = 50, choices = APPROVAL_STATUS_CHOICES, default = 'pending')
    disapproval_reason = models.TextField(blank = True, null = True)
    withdraw        = models.BooleanField(default = False, verbose_name = 'Withdraw') 
    is_featured     = models.BooleanField("Featured", default = False)
    is_verified     = models.BooleanField("Verified", default = False)
    is_active       = models.BooleanField("Active", default = True)
    is_locked       = models.BooleanField("Locked", default = False)
    locked_reason   = models.CharField(max_length = 255, blank = True, null = True)
    discount_available = models.BooleanField(default = False)
    discount_description = models.CharField(max_length = 255, blank=True, null=True)
    discount_percentage_off = models.PositiveSmallIntegerField(blank=True, null=True)
    # discount_starts = models.DateTimeField(blank = True, null=True)
    discount_ends   = models.DateTimeField(blank = True, null=True)
    view_count      = models.PositiveSmallIntegerField(default=0)
    enquiry_count   = models.PositiveSmallIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.name}-{self.created_at.strftime('%d/%m/%Y')}"

    def get_absolute_url(self):
        return reverse('listings:public-property-details', args=[ str(self.slug), str(self.id)])

    def get_listing_details(self):
        return reverse('listings:listing-details', args=[str(self.id)])

    def get_hx_url(self):
        return reverse('listings:listing-hx-details', kwargs={'id': self.id})
    
    def get_edit_url(self):
        return reverse('listings:listing-update', args=[str(self.id)])
    
    def get_withdraw_url(self):
        return reverse('listings:listing-withdraw', args=[str(self.id)])

    def get_spec_children(self):
        return self.listingspecification_set.all()

    def get_nearbys_children(self):
        return self.listingnearby_set.all()

    def get_sqft(self):
        sqft = self.length * self.breadth
        return sqft

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def slugify_instance_address(instance, save=False, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.address)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = random.randint(1_000_000, 2_000_000)
        slug = f"{slug}-{rand_int}"
        return slugify_instance_address(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def listing_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
       slugify_instance_address(instance, save=False)


pre_save.connect(listing_pre_save, sender = Listing)


def listing_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_address(instance, save=True)
        
post_save.connect(listing_post_save, sender = Listing)


class ListingType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField("Active", default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listing_types')

    class Meta:
        verbose_name = 'Property Type'
        verbose_name_plural = 'Property Types'

    def __str__(self):
        return str(self.name)


class ListingPicture(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to = 'pictures/properties/', blank=True, null=True,
            validators = [validate_picture_size, validate_picture_dimension])#, validate_picture_dimension(width=575, height=365)])
    is_feature = models.BooleanField("Featured", default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Property Picture"


class ListingVideo(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    video = models.FileField(upload_to = 'videos/properties/', blank=True, null=True,
            validators = [validate_video_size])
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return str(self.listing)

    class Meta:
        verbose_name = "Property Video"


class ListingFloor(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    FLOOR_CHOICES = (
        ('ground', '0 Floor'),
        ('first', '1st Floor'),
        ('second', '2nd Floor'),
        ('third', '3rd Floor'),
        ('fourth', '4th Floor'),
        ('fifth', '5th Floor'),
        ('sixth', '6th Floor'),
        ('seventh', '7th Floor'),
        ('eight', '8th Floor'),
        ('ninth', '9th Floor'),
        ('tenth', '10th Floor'),
    )    
    floor = models.CharField(max_length=15, choices=FLOOR_CHOICES)
    BEDROOM_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    number_of_rooms = models.CharField('Rooms', max_length=2, choices=BEDROOM_CHOICES)
    RESTROOM_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rest_rooms = models.CharField('Bathroom', max_length=2, choices=RESTROOM_CHOICES)
    PARLOR_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    parlor = models.CharField(max_length=2, choices=PARLOR_CHOICES, default='0')
    STORE_CHOICES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    store = models.CharField(max_length=2, choices=PARLOR_CHOICES, default='0')
    floor_plan = models.ImageField('Plan', upload_to = 'pictures/floor_plans/', validators = [validate_floor_design_size], blank=True, null=True) 
    # Dimension of the floor plant pics is height 575 and width 364
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return str(self.floor)

    class Meta:
        verbose_name = "Property Floor"


class ListingAttribute(models.Model):
    listing_type = models.ForeignKey(ListingType, verbose_name = "Property type", on_delete=models.CASCADE)
    name = models.CharField("Attribute name", max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Property Attribute"


class ListingSpecification(models.Model):
    listing = models.ForeignKey(Listing, verbose_name = "Property", on_delete = models.CASCADE)
    attribute = models.ForeignKey(ListingAttribute, verbose_name = 'Specification', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name = 'Value', blank=True, null = True)

    def __str__(self):
        return f'{self.attribute} - {self.value}'

    class Meta:
        verbose_name = "Property Specification"

    def get_absolut_url(self):
        return self.listing.get_absolute_url()

    def get_hx_edit_url(self):
        kwargs = {
            'parent_id': self.listing.id,
            'id': self.id
        }
        return reverse('listings:hx-spec-detail', kwargs=kwargs)


class ListingFeature(models.Model):
    # listing_type = models.ForeignKey(ListingType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Property Feature"


class ListingAdditionalFeature(models.Model):
    listing = models.ForeignKey(Listing, verbose_name = 'Property', on_delete = models.CASCADE)
    feature = models.ManyToManyField(ListingFeature, verbose_name = 'Property feature')

    def __str__(self):
        return str(self.feature)

    class Meta:
        verbose_name = "Additional Feature"


class NearbyCategory(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Nearby Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ListingNearby(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    category = models.ForeignKey(NearbyCategory, on_delete=models.CASCADE, blank=True, null=True, related_name='category')
    name = models.CharField(max_length=120, blank = True, null = True)
    location = models.CharField(max_length=50, blank=True, null=True)
    approximate_distance = models.PositiveSmallIntegerField('Distance',blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # def get_absolute_url(self):
    #     return reverse('listings:listing_nearby_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.listing)

    class Meta:
        verbose_name = "Places Nearby"