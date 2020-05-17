"""Deals with order queries
"""
from orders.models import OrderItem, Order


def create_order_item(data_dict):
    """Create an order item from items provided

    Arguments:
        data_dict {dictionary} -- contains the data for an order item
    """
    item = OrderItem(**data_dict)
    item.save()


def get_order(order_id):
    """Fetch an order

    Arguments:
        order_id {int} -- id of order to fetch
    """
    return Order.objects.get(id=order_id)
