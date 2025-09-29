import logging
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from .models import Panier
from moncashify import API

logger = logging.getLogger(__name__)

def panier_context(request):
    """
    Fournit le panier, le total, le compteur et le lien de paiement MonCash.
    """

    # ✅ S'assurer que la session existe
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    # ✅ Récupération du panier
    panier = Panier.objects.filter(session_id=session_id)
    total = sum(item.produit.prix * item.quantite for item in panier)
    panier_count = sum(item.quantite for item in panier)

    # Calcul du total individuel pour chaque item
    for item in panier:
        item.total = item.produit.prix * item.quantite

    payment_url = None
    if total > 0:
        try:
            # ✅ Conversion en float accepté par MonCash
            amount = float(
                Decimal(total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            )

            moncash_api = API(
                client_id=settings.MONCASH_CLIENT_ID,
                secret_key=settings.MONCASH_SECRET_ID,
                debug=getattr(settings, "MONCASH_DEBUG", True)
            )

            payment = moncash_api.payment(
                order_id=f"order-{session_id}",
                amount=amount
            )
            payment_url = payment.redirect_url

        except Exception as e:
            logger.error(f"[MonCash] Erreur lors de la génération du paiement : {e}")
            payment_url = None

    return {
        "panier": panier,
        "panier_count": panier_count,
        "total": total,
        "payment_url": payment_url
    }
