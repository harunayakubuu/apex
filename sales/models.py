from django.db import models
from listings.models import Listing
from django.utils import timezone
from clients.models import Client, Customer
from .utils import generate_code
from django.shortcuts import reverse


class Position(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE)
    price = models.PositiveIntegerField(blank = True)
    commission = models.DecimalField(decimal_places=1, max_digits=3)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def save(self, *args, **kwargs):
        if self.listing.price:
            self.price = self.listing.price
        else:
            self.price = 0

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.id}, property: {self.listing.name}"


class Sale(models.Model):
    transaction_id = models.CharField(max_length = 64, blank = True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(blank=True, null = True)
    commission = models.PositiveIntegerField(blank=True, null = True)
    total_price = models.PositiveIntegerField(blank=True, null = True)
    buyer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    created = models.DateTimeField(blank = True)
    updated = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"Sale of {self.position.listing.name} for the price: {self.price}, and commission: {self.commission}, total amount of: {self.total_price}"

    def get_absolute_url(self):
        return reverse('sales:sales-detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if self.transaction_id == '':
            self.transaction_id = generate_code()
        if self.created == None:
            self.created = timezone.now()

        self.price = self.position.price

        if self.commission == None:
            if self.position.listing.discount_percentage_off: 
                raw_commission = self.position.price * (self.position.commission / 100)
                percentage_off = raw_commission * (self.position.listing.discount_percentage_off / 100)
                self.commission = raw_commission - percentage_off
            else:
                self.commission = self.position.price * (self.position.commission / 100)

        self.total_price = self.price + self.commission

        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()


class CSV(models.Model):
    file_name = models.FileField(upload_to = 'csvs')
    activated = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return str(self.file_name)

    class Meta:
        verbose_name_plural = "CSVs"