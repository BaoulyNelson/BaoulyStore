"""
Catalogue services — business logic separated from views.

All queryset-heavy operations that go beyond a simple .filter() live here,
keeping views thin and making logic independently testable.
"""
from django.core.paginator import Paginator, Page
from django.db.models import QuerySet

from .models import Produit

# ---------------------------------------------------------------------------
# Selectors (read operations)
# ---------------------------------------------------------------------------

PAGE_SIZE_DEFAULT = 100


def get_produits_page(categorie: str | None = None, page_number=1, per_page: int = PAGE_SIZE_DEFAULT) -> Page:
    """Return a paginated page of products, optionally filtered by category."""
    qs = Produit.objects.all() if not categorie else Produit.objects.par_categorie(categorie)
    return Paginator(qs, per_page).get_page(page_number)


def get_produits_populaires(limit: int = 9) -> QuerySet:
    return Produit.objects.populaires()[:limit]


def get_produits_nouveaux(limit: int = 9) -> QuerySet:
    return Produit.objects.nouveaux()[:limit]


def get_produits_similaires(produit: Produit, limit: int = 8) -> QuerySet:
    return (
        Produit.objects
        .par_categorie(produit.categorie)
        .exclude(pk=produit.pk)[:limit]
    )


def search_produits(query: str) -> QuerySet:
    """Search products by display label (choices) and description."""
    if not query or not query.strip():
        return Produit.objects.none()
    q = query.strip()
    return Produit.objects.filter(description__icontains=q) | Produit.objects.filter(nom__icontains=q)


# ---------------------------------------------------------------------------
# Writers (write operations)
# ---------------------------------------------------------------------------

def create_produit(validated_data: dict) -> Produit:
    return Produit.objects.create(**validated_data)


def update_produit(produit: Produit, validated_data: dict) -> Produit:
    for field, value in validated_data.items():
        setattr(produit, field, value)
    produit.save()
    return produit
