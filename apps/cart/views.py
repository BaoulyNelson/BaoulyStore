"""
Cart views — add, view, update quantity, remove, and MonCash checkout.
All business logic is delegated to cart.services.
"""
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.catalogue.models import Produit
from . import services
from .models import CartItem

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Cart views
# ---------------------------------------------------------------------------

@login_required
def add_to_cart(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)

    if produit.quantite_en_stock <= 0:
        messages.warning(request, "Ce produit est en rupture de stock.")
        return redirect(reverse('cart:view') + '?open_cart=1')

    session_id = services.get_or_create_session(request)
    item, added = services.add_to_cart(session_id, produit)

    if added or item.quantite <= produit.quantite_en_stock:
        messages.success(request, f"« {produit.get_nom_display()} » ajouté au panier.")
    else:
        messages.warning(request, "Stock insuffisant.")

    count = services.get_cart_count(session_id)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': count})

    return redirect(reverse('cart:view') + '?open_cart=1')



def view_cart(request):
    """Display the cart and generate a MonCash payment link."""
    session_id = services.get_or_create_session(request)
    cart_items = services.get_cart(session_id)
    total = services.get_cart_total(session_id)
    payment_url = None
    error_message = None

    if total > 0:
        payment_url = services.create_moncash_payment(total)
        if not payment_url:
            error_message = "Le service de paiement est temporairement indisponible. Veuillez réessayer."

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'cart_total': total,
        'payment_url': payment_url,
        'error_message': error_message,
    })


@login_required
def update_quantity(request, produit_id, quantite):
    session_id = services.get_or_create_session(request)
    try:
        item = services.update_item_quantity(session_id, produit_id, quantite)
        total = services.get_cart_total(session_id)
        return JsonResponse({
            'item_total': float(item.subtotal),
            'total':      float(total),
            'cart_count': services.get_cart_count(session_id),
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Article introuvable.'}, status=404)

@login_required
def remove_from_cart(request, produit_id):
    """Remove a product from the cart."""
    produit = get_object_or_404(Produit, pk=produit_id)

    if request.method == 'POST':
        session_id = services.get_or_create_session(request)
        services.remove_from_cart(session_id, produit_id)
        messages.success(request, f"« {produit.get_nom_display()} » retiré du panier.")
        return redirect('cart:view')

    # GET → show confirmation page
    return render(request, 'cart/confirm_remove.html', {'produit': produit})
