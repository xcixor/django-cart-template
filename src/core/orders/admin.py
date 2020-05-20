"""Admin page for orders
"""
import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    """Download order list as csv

    Arguments:
        modeladmin {object} -- Instance of the current model admin
        being displayed
        request {object} -- The current request object as an
        HttpRequest instance
        queryset {[type]} -- A QuerySet for the objects selected by the user

    Returns:
        [type] -- [description]
    """
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many
              and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    """Takes an Order object as an argument and returns an
    HTML link for the admin_order_detail URL

    Arguments:
        obj {object} -- object to generate html link for

    Returns:
        string -- html link
    """
    return mark_safe('<a href="{}">View</a>'
                     .format(reverse('orders:admin_order_detail',
                                     args=[obj.id])))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Manages orders.
    """
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city', 'paid',
        'created', 'updated', order_detail
        ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    extra = 1
    actions = [export_to_csv]