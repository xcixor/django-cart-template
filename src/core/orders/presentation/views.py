from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse
from orders.forms import OrderCreateForm
from cart.cart import Cart
from orders.data import create_order_item, get_order
from orders.task import order_created


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
                # launch asynchronous task
                order_created.delay(order.id)
                # set the order in the session
                request.session['order_id'] = order.id
                # redirect for payment
                return redirect(reverse('payment:process'))
            return redirect('/cart')
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    """Custom admin view to display information about an order

    Arguments:
        request {object} -- django request object (http)
        order_id {int} -- id of order to display

    Returns:
        object -- django http response
    """
    order = get_order(order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
