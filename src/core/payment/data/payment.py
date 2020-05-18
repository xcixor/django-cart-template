"""Contains functionality to query db for payments related data.
"""
from django.shortcuts import get_object_or_404
from orders.models import Order


def get_order(order_id):
    """Fetch order to pay for.

    Arguments:
        order_id {int} -- id of the order to fetch
    """
    return get_object_or_404(Order, id=order_id)
