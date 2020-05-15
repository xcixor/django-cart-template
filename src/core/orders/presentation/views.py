from django.shortcuts import render, redirect
from orders.forms import OrderCreateForm
from cart.cart import Cart
from orders.data import create_order_item


def order_create(request):
    """Create order item from user data

    Arguments:
        request {[type]} -- [description]

    Returns:
        object -- http response
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            if cart:
                order = form.save()
                for item in cart:
                    data_dict = {
                        'order': order,
                        'product': item['product'],
                        'price': item['price'],
                        'quantity': item['quantity']
                    }
                    create_order_item(data_dict)
                # clear the cart
                cart.clear()
                return render(
                    request,
                    'orders/order/created.html',
                    {'order': order})
            return redirect('/cart')
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})
