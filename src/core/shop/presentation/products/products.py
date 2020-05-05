"""Defines views related to products
"""
from django.shortcuts import render
from shop.application import get_product_list, get_product_detail


def product_list(request, category_slug=None):
    """Render products page

    Arguments:
        request {object} -- django http request object
        category_slug {string} -- parameter to optionally filter products by
            category (default: {None})
    """
    return render(
        request,
        "shop/product/list.html",
        get_product_list(category_slug)
    )


def product_detail(request, product_id, slug):
    """Render the product details page

    Arguments:
        request {[type]} -- [description]
        product_id {int} -- id of the product to render
        slug {string} -- the url of the product to render

    Returns:
        object -- html content
    """
    return render(
        request,
        'shop/product/detail.html',
        {'product': get_product_detail(product_id, slug)}
    )
