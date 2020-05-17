"""forms for managing the cart
"""
from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """Adds a product to the cart

    Arguments:
        forms {object} -- form object
    """
    quantity = forms.ChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES)
    update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput)
