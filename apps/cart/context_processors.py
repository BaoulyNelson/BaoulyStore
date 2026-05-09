"""
Cart context processor.

Provides cart count and total to every template.
MonCash payment URL is deliberately NOT generated here — it would trigger
an external API call on every single page load, which is unacceptable.
The payment URL is generated only when the user views the cart page.
"""
from .services import get_or_create_session, get_cart, get_cart_count, get_cart_total

def cart_context(request):
    session_id = get_or_create_session(request)
    cart_items = get_cart(session_id)

    # Plus besoin d'annoter manuellement : item.subtotal est déjà
    # une @property définie sur CartItem.

    return {
        'cart_items': cart_items,
        'cart_count': get_cart_count(session_id),
        'cart_total': get_cart_total(session_id),
    }