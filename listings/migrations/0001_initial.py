# Generated by Django 3.2.12 on 2023-07-18 13:59

from django.db import migrations, models
import django.db.models.deletion
import listings.validators
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('clients', '0001_initial'),
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='listings.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Property name')),
                ('price', models.PositiveIntegerField(blank=True, help_text='in Nigerian naira #', null=True)),
                ('price_status', models.CharField(blank=True, choices=[('fixed', 'Fixed Price'), ('negotiable', 'Price Negoiable')], default='negotiable', max_length=255, null=True)),
                ('status', models.CharField(choices=[('rent', 'For Rent'), ('sale', 'For Sale')], default='sale', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('length', models.PositiveIntegerField(help_text='Length of plot in feet. E.g 50', verbose_name='Length of Plot')),
                ('breadth', models.PositiveIntegerField(help_text='Breadth of plot in feet. E.g 50', verbose_name='Breadth of Plot')),
                ('address', models.CharField(max_length=255, verbose_name='Property address')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('location', models.CharField(max_length=255, verbose_name='Property Location')),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
                ('city', models.CharField(max_length=255, verbose_name='City/Town')),
                ('state', models.CharField(choices=[('FCT', 'Abuja'), ('Abia', 'Abia'), ('Adamawa', 'Adamawa'), ('AkwaIbom', 'Akwa Ibom'), ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'), ('CrossRiver', 'Cross River'), ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara')], max_length=20, verbose_name='State')),
                ('encumbrances', models.BooleanField(default=False, help_text='Check the box if this property is under any encumbrances. Eg. Bank loan.', verbose_name='Is there any encumbrances on this property?')),
                ('encumbrance_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Encumbrance description')),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default='pending', max_length=50)),
                ('disapproval_reason', models.TextField(blank=True, null=True)),
                ('withdraw', models.BooleanField(default=False, verbose_name='Withdraw')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Verified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_locked', models.BooleanField(default=False, verbose_name='Locked')),
                ('locked_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('discount_available', models.BooleanField(default=False)),
                ('discount_description', models.CharField(blank=True, max_length=255, null=True)),
                ('discount_percentage_off', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('discount_ends', models.DateTimeField(blank=True, null=True)),
                ('view_count', models.PositiveSmallIntegerField(default=0)),
                ('enquiry_count', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listings.category')),
                ('listing_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent', to='agents.agent')),
                ('listing_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='clients.client')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ListingAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Attribute name')),
            ],
            options={
                'verbose_name': 'Property Attribute',
            },
        ),
        migrations.CreateModel(
            name='ListingFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Property Feature',
            },
        ),
        migrations.CreateModel(
            name='NearbyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'verbose_name_plural': 'Nearby Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ListingVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/properties/', validators=[listings.validators.validate_video_size])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('listing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
            options={
                'verbose_name': 'Property Video',
            },
        ),
        migrations.CreateModel(
            name='ListingType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_types', to='listings.category')),
            ],
            options={
                'verbose_name': 'Property Type',
                'verbose_name_plural': 'Property Types',
            },
        ),
        migrations.CreateModel(
            name='ListingSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Value')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listingattribute', verbose_name='Specification')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing', verbose_name='Property')),
            ],
            options={
                'verbose_name': 'Property Specification',
            },
        ),
        migrations.CreateModel(
            name='ListingPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='pictures/properties/', validators=[listings.validators.validate_picture_size, listings.validators.validate_picture_dimension])),
                ('is_feature', models.BooleanField(default=False, verbose_name='Featured')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
            options={
                'verbose_name': 'Property Picture',
            },
        ),
        migrations.CreateModel(
            name='ListingNearby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('approximate_distance', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Distance')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='listings.nearbycategory')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
            options={
                'verbose_name': 'Places Nearby',
            },
        ),
        migrations.CreateModel(
            name='ListingFloor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(choices=[('ground', '0 Floor'), ('first', '1st Floor'), ('second', '2nd Floor'), ('third', '3rd Floor'), ('fourth', '4th Floor'), ('fifth', '5th Floor'), ('sixth', '6th Floor'), ('seventh', '7th Floor'), ('eight', '8th Floor'), ('ninth', '9th Floor'), ('tenth', '10th Floor')], max_length=15)),
                ('number_of_rooms', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=2, verbose_name='Rooms')),
                ('rest_rooms', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=2, verbose_name='Bathroom')),
                ('parlor', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], default='0', max_length=2)),
                ('store', models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3')], default='0', max_length=2)),
                ('floor_plan', models.ImageField(blank=True, null=True, upload_to='pictures/floor_plans/', validators=[listings.validators.validate_floor_design_size], verbose_name='Plan')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
            options={
                'verbose_name': 'Property Floor',
            },
        ),
        migrations.AddField(
            model_name='listingattribute',
            name='listing_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listingtype', verbose_name='Property type'),
        ),
        migrations.CreateModel(
            name='ListingAdditionalFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.ManyToManyField(to='listings.ListingFeature', verbose_name='Property feature')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing', verbose_name='Property')),
            ],
            options={
                'verbose_name': 'Additional Feature',
            },
        ),
        migrations.AddField(
            model_name='listing',
            name='listing_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='listings.listingtype'),
        ),
        migrations.AddField(
            model_name='listing',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
    ]