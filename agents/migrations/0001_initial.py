# Generated by Django 3.2.12 on 2023-07-18 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import listings.validators
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='additional Phone Number')),
                ('profile_picture', models.ImageField(blank=True, help_text="Displayed on your account's profile", null=True, upload_to='pictures/agents/profile-pictures/', validators=[listings.validators.validate_picture_size])),
                ('display_picture', models.ImageField(blank=True, help_text='Displayed to the public', null=True, upload_to='pictures/agents/display-pictures/', validators=[listings.validators.validate_picture_size])),
                ('about', models.TextField(blank=True, null=True)),
                ('agent_of_the_week', models.BooleanField(default=False)),
                ('agent_of_the_month', models.BooleanField(default=False)),
                ('agent_of_the_year', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('hire_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]