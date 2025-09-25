import uuid
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings
from patterns.models import Pattern

# Create your models here.


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=Decimal("0.00")
    )

    def _generate_order_number(self):
        ''' Generate random number for the order number '''
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update the order_total from related line items."""
        total = self.lineitems.aggregate(
            sum=Sum("lineitem_total")
        )["sum"] or Decimal("0.00")
        self.order_total = total
        self.save(update_fields=["order_total"])

    def save(self, *args, **kwargs):
        '''
        Overrides original save method to set the order number if it hasn't
        been set yet
        '''
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    pattern = models.ForeignKey(
        Pattern,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """Calculate and update line total for Loop & Thread checkout."""
        self.lineitem_total = self.pattern.price
        super().save(*args, **kwargs)
        self.order.update_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total()

    def __str__(self):
        return f"Loop & Thread Line Item for order {self.order.order_number}"
