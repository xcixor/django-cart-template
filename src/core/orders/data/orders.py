"""Deals with order queries
"""
from orders.models import OrderItem


def create_order_item(data_dict):
    """Create an order item from items provided

    Arguments:
        data_dict {dictionary} -- contains the data for an order item
    """
    item = OrderItem(**data_dict)
    item.save()
