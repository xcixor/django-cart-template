"""contains cart views
"""
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from cart.cart import Cart
from cart.forms import CartAddProductForm
from cart.application import get_product
from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    """view to add products or update their quantities

    Arguments:
        request {object} -- django request object
        product_id {int} -- id of product to add or edit

    Returns:
        object -- django http response
    """
    cart = Cart(request)
    product = get_product(product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
            )
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """removes an item from the cart

    Arguments:
        request {object} -- django http request object
        product_id {int} -- id of item to remove

    Returns:
        object -- http response
    """
    cart = Cart(request)
    product = get_product(product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Displays the cart items

    Arguments:
        request {object} -- django http request object

    Returns:
        object -- http response
    """
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html',
                  {
                      'cart': cart,
                      'coupon_apply_form': coupon_apply_form
                      })
