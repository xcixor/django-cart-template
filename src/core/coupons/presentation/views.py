"""Contains coupon relates views."""
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
from coupons.data import get_valid_coupon


@require_POST
def coupon_apply(request):
    """Validates user coupon and saves it in the user's session.
    """
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        coupon = get_valid_coupon(code)
        if coupon:
            request.session['coupon_id'] = coupon.id
        else:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
