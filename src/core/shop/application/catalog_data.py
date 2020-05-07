"""fetch catalog data
"""
from django.shortcuts import get_object_or_404
from shop.models import Category, Product


def get_product_list(category_slug=None):
    """Fetch catalog products

    Keyword Arguments:
        category_slug {string} -- parameter to optionally filter products by
        category (default: {None})
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products
        }
    return context


def get_product_detail(product_id, slug):
    """Fetch product details

    Arguments:
        product_id {int} -- id of product to fetch
        slug {string} -- url of the product

    Returns:
        product -- the matching object
    """
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    return product
