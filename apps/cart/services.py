"""
Cart services — all cart business logic and MonCash integration.

MonCash calls are intentionally NOT made in the context processor.
The payment URL is only generated when the user visits the cart page,
preventing an API call on every single page load.
"""
import uuid
import logging
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings

from .models import CartItem

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------

def get_or_create_session(request) -> str:
    """Ensure the session has a key and return it."""
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


# ---------------------------------------------------------------------------
# Cart selectors
# ---------------------------------------------------------------------------

def get_cart(session_id: str):
    return CartItem.objects.for_session(session_id)


def get_cart_total(session_id: str) -> float:
    return CartItem.objects.total_for_session(session_id)


def get_cart_count(session_id: str) -> int:
    return CartItem.objects.count_for_session(session_id)


# ---------------------------------------------------------------------------
# Cart mutations
# ---------------------------------------------------------------------------

from django.db.models import F
from apps.catalogue.models import Produit

def add_to_cart(session_id: str, produit) -> tuple[CartItem, bool]:
    """Add one unit of *produit* to the cart. Returns (item, added)."""
    item, created = CartItem.objects.get_or_create(
        session_id=session_id,
        produit=produit,
    )
    if created:
        # Nouvelle ligne — quantite = 1 (défaut du modèle), on décrémente le stock
        Produit.objects.filter(pk=produit.pk).update(
            quantite_en_stock=F('quantite_en_stock') - 1
        )
        return item, True

    # Article déjà dans le panier
    if item.quantite < produit.quantite_en_stock:
        item.quantite += 1
        item.save(update_fields=['quantite'])
        Produit.objects.filter(pk=produit.pk).update(
            quantite_en_stock=F('quantite_en_stock') - 1
        )
        return item, False

    # Stock épuisé — on ne touche rien
    return item, False


def update_item_quantity(session_id: str, produit_id: int, quantite: int) -> CartItem:
    """Set the quantity of a cart item. Adjusts stock by the difference."""
    item = CartItem.objects.select_related('produit').get(
        session_id=session_id,
        produit_id=produit_id,
    )

    ancienne_quantite = item.quantite
    difference = quantite - ancienne_quantite  # positif = on prend du stock, négatif = on rend

    if quantite <= 0:
        # Restituer tout le stock de cet article
        Produit.objects.filter(pk=produit_id).update(
            quantite_en_stock=F('quantite_en_stock') + ancienne_quantite
        )
        item.delete()
        raise CartItem.DoesNotExist("Item removed because quantity was 0.")

    item.quantite = quantite
    item.save(update_fields=['quantite'])

    # Ajuster le stock selon la différence
    Produit.objects.filter(pk=produit_id).update(
        quantite_en_stock=F('quantite_en_stock') - difference
    )

    return item


def remove_from_cart(session_id: str, produit_id: int) -> None:
    """Remove item and restore its stock."""
    try:
        item = CartItem.objects.get(session_id=session_id, produit_id=produit_id)
        quantite_a_restituer = item.quantite
        item.delete()
        Produit.objects.filter(pk=produit_id).update(
            quantite_en_stock=F('quantite_en_stock') + quantite_a_restituer
        )
    except CartItem.DoesNotExist:
        pass


def clear_cart(session_id: str) -> None:
    """Remove all items and restore all their stock."""
    items = CartItem.objects.filter(session_id=session_id).select_related('produit')
    for item in items:
        Produit.objects.filter(pk=item.produit_id).update(
            quantite_en_stock=F('quantite_en_stock') + item.quantite
        )
    items.delete()
# ---------------------------------------------------------------------------
# MonCash integration
# ---------------------------------------------------------------------------

def create_moncash_payment(total: float, order_id: str | None = None) -> str | None:
    """
    Create a MonCash payment and return the redirect URL.

    Returns None on any error (logged). Callers should handle None gracefully.
    This function is called only from views/cart — never from context processors.
    """
    if not settings.MONCASH_CLIENT_ID or not settings.MONCASH_SECRET_ID:
        logger.error("[MonCash] MONCASH_CLIENT_ID or MONCASH_SECRET_ID not configured.")
        return None

    if total <= 0:
        logger.warning("[MonCash] Attempted payment with total <= 0.")
        return None

    try:
        from moncashify import API  # lazy import to avoid startup overhead
        amount = float(
            Decimal(str(total)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        )
        oid = order_id or f"order-{uuid.uuid4().hex[:12]}"
        api = API(
            client_id=settings.MONCASH_CLIENT_ID,
            secret_key=settings.MONCASH_SECRET_ID,
            debug=settings.MONCASH_DEBUG,
        )
        payment = api.payment(order_id=oid, amount=amount)
        url = getattr(payment, 'redirect_url', None) or getattr(payment, 'payment_url', None)
        if not url:
            logger.error("[MonCash] Payment created but no URL returned. Attrs: %s", dir(payment))
        return url
    except Exception as exc:
        logger.error("[MonCash] Payment creation failed: %s", exc, exc_info=True)
        return None
