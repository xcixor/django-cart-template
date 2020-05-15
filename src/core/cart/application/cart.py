"""contains cart related data
"""
from django.shortcuts import get_object_or_404
from shop.models import Product


def get_product(product_id):
    """fetch object instance to add to cart

    Arguments:
        product_id {int} -- id of product to fetch

    Returns:
        object -- fetched product instance
    """
    return get_object_or_404(Product, id=product_id)


def get_products(product_ids):
    """Get products from ids

    Arguments:
        product_ids {disctionary} -- dictionary containing a list of keys to
        fetch products with
    """
    return Product.objects.filter(id__in=product_ids)
