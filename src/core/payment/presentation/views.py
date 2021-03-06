"""Contains payment views.
"""
from io import BytesIO
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
import braintree
from django.shortcuts import render, redirect
from payment.data import get_order


# investigate how to make this view more secure
# maybe the nonce token and other tokens should be converted to
# some encrypted format such as in confirm email token in teke
# also integrate paypal(dropin ui from braintree) and mpesa
def payment_process(request):
    """Checkout user order with payment.

    Arguments:
        request {object} -- django httprequest
    """
    order_id = request.session.get('order_id')
    order = get_order(order_id)
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            send_order_confirmation_email(order)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(
            request,
            'payment/process.html',
            {
                'order': order,
                'client_token': client_token
            }
        )


def payment_done(request):
    """Renders the payment successful page.
    """
    return render(request, 'payment/done.html')


def payment_canceled(request):
    """Renders the payment cancelled page.
    """
    return render(request, 'payment/canceled.html')


def send_order_confirmation_email(order):
    # create invoice e-mail
    subject = 'My Shop - Invoice no. {}'.format(order.id)
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/orders/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach(
        'order_{}.pdf'.format(order.id),
        out.getvalue(),
        'application/pdf'
        )
    # send e-mail
    email.send()
