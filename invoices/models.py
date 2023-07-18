import uuid
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse

from listings.models import Listing
from clients.models import Client

from sales.models import Position, Sale


class Invoice(models.Model):
    invoice_id = models.CharField(max_length = 64, blank = True)
    # position = models.ForeignKey(Position, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return str(self.invoice_id)

    def get_absolute_url(self):
        return reverse('invoices:invoice_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if self.invoice_id == '':
            self.invoice_id = code = str(uuid.uuid4()).upper().split('-')[4]
        if self.created == None:
            self.created = timezone.now()

        # if self.commission == None:
        #     self.commission = self.position.price * (self.position.commission / 100)

        # self.total_price = self.price + self.commission

        return super().save(*args, **kwargs)