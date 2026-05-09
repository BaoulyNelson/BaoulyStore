from django.contrib import admin, messages
from django.db.models import Sum
from django.utils.html import format_html
from .models import CartItem


# ---------------------------------------------------------------------------
# Actions groupées
# ---------------------------------------------------------------------------

@admin.action(description='🗑️ Vider les paniers sélectionnés')
def vider_paniers(modeladmin, request, queryset):
    sessions = queryset.values_list('session_id', flat=True).distinct()
    deleted, _ = CartItem.objects.filter(session_id__in=sessions).delete()
    modeladmin.message_user(request, f'{deleted} article(s) supprimé(s) sur {len(sessions)} session(s).', messages.SUCCESS)


@admin.action(description='➕ Mettre la quantité à 1')
def reset_quantite(modeladmin, request, queryset):
    updated = queryset.update(quantite=1)
    modeladmin.message_user(request, f'Quantité remise à 1 pour {updated} article(s).', messages.SUCCESS)


@admin.action(description='❌ Supprimer les articles sélectionnés')
def supprimer_articles(modeladmin, request, queryset):
    count = queryset.count()
    queryset.delete()
    modeladmin.message_user(request, f'{count} article(s) supprimé(s) du panier.', messages.SUCCESS)


# ---------------------------------------------------------------------------
# Inline — voir les articles d'une session depuis une vue groupée
# ---------------------------------------------------------------------------

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('produit', 'quantite', 'subtotal_display', 'date_ajout')
    can_delete = True

    @admin.display(description='Sous-total')
    def subtotal_display(self, obj):
        return f'{obj.subtotal:,.2f} HTG'


# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('produit', 'session_courte', 'quantite', 'subtotal_display', 'date_ajout')
    list_display_links = ('produit',)
    list_filter = ('date_ajout', 'produit__categorie')
    search_fields = ('session_id', 'produit__description')
    ordering = ('-date_ajout',)
    readonly_fields = ('date_ajout', 'subtotal_display')
    actions = [
        vider_paniers,
        reset_quantite,
        supprimer_articles,
    ]
    fieldsets = (
        ('Article', {
            'fields': ('produit', 'quantite', 'subtotal_display')
        }),
        ('Session', {
            'fields': ('session_id', 'date_ajout')
        }),
    )

    @admin.display(description='Session')
    def session_courte(self, obj):
        """Affiche les 12 premiers caractères du session_id pour lisibilité."""
        return format_html(
            '<code title="{}">{}</code>',
            obj.session_id,
            obj.session_id[:12] + '…',
        )

    @admin.display(description='Sous-total')
    def subtotal_display(self, obj):
        return f'{obj.subtotal:,.2f} HTG'