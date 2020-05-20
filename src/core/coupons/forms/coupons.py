"""Contains coupons related forms."""
from django import forms


class CouponApplyForm(forms.Form):
    """Collects user coupon.
    """
    code = forms.CharField()
