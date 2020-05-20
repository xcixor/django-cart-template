"""Queries for coupon related data."""
from django.utils import timezone
from coupons.models import Coupon


def get_valid_coupon(code):
    """Get valid coupon from db

    Arguments:
        code {string} -- coupon to validate as entered by user.
    """
    now = timezone.now()
    try:
        coupon = Coupon.objects.get(
            code__iexact=code,
            valid_from__lte=now,
            valid_to__gte=now,
            active=True)
        return coupon
    except Coupon.DoesNotExist:
        return None


def get_coupon(coupon_id):
    """Get coupon.

    Arguments:
        coupon_id {int} -- coupon to fetch
    """
    return Coupon.objects.get(id=coupon_id)
