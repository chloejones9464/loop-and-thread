from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.


class OrderLineAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline,)

    readonly_fields = ('order_number', 'date', 'order_total')

    fields = (
        'order_number', 'date', 'full_name', 'email', 'phone_number',
        'country', 'postcode', 'town_or_city', 'street_address1',
        'street_address2', 'county', 'order_total',
    )

    list_display = (
        'order_number', 'date', 'full_name', 'order_total',
    )

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
