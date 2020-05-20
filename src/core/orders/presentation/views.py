from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
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
                order = form.save(commit=False)
                if cart.coupon:
                    order.coupon = cart.coupon
                    order.discount = cart.coupon.discount
                order.save()
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


@staff_member_required
def admin_order_pdf(request, order_id):
    """Generates a pdf invoice for existing order

    Arguments:
        request {object} -- django http request object
        order_id {int} -- id of order to print

    Returns:
        object -- http response
    """
    order = get_order(order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.\
        format(order.id)
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT +
                                    'css/orders/pdf.css')])
    return response
