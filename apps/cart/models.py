from django.db import models
from apps.catalogue.models import Produit


class CartManager(models.Manager):
    def for_session(self, session_id: str):
        return self.filter(session_id=session_id).select_related('produit')

    def total_for_session(self, session_id: str) -> float:
        items = self.for_session(session_id)
        return float(sum(item.produit.prix * item.quantite for item in items))

    def count_for_session(self, session_id: str) -> int:
        from django.db.models import Sum
        result = self.filter(session_id=session_id).aggregate(total=Sum('quantite'))
        return result['total'] or 0


class CartItem(models.Model):
    """
    A cart item tied to an anonymous session.

    NOTE: The cart is session-based. For a richer experience (persistent
    carts across devices), consider migrating to a user-based cart later.
    """
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        verbose_name='Produit',
        related_name='cart_items',
    )
    quantite = models.PositiveIntegerField(default=1, verbose_name='Quantité')
    session_id = models.CharField(max_length=255, db_index=True, verbose_name='Session ID')
    date_ajout = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    class Meta:
        verbose_name = 'Article du panier'
        verbose_name_plural = 'Articles du panier'
        ordering = ['-date_ajout']
        # Ensure one row per (session, product)
        unique_together = [('session_id', 'produit')]

    def __str__(self) -> str:
        return f"{self.quantite} × {self.produit}"

    @property
    def subtotal(self):
        return self.produit.prix * self.quantite
