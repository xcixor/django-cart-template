from .cart import Cart


def cart(request):
    """Returns a dictionary of objects that will be available
        to all the templates rendered using RequestContext. The
        point is to make the cart globally avaialable in the application

    Arguments:
        request {object} -- django request object

    Returns:
        dictionary -- Users cart containing their shopping
    """
    return {'cart': Cart(request)}
