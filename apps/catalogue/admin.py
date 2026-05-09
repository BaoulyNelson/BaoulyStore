from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Produit


# ---------------------------------------------------------------------------
# Actions groupées
# ---------------------------------------------------------------------------

@admin.action(description='✅ Marquer comme populaire')
def marquer_populaire(modeladmin, request, queryset):
    updated = queryset.update(populaire=True)
    modeladmin.message_user(request, f'{updated} produit(s) marqué(s) comme populaire.', messages.SUCCESS)


@admin.action(description='❌ Retirer des populaires')
def retirer_populaire(modeladmin, request, queryset):
    updated = queryset.update(populaire=False)
    modeladmin.message_user(request, f'{updated} produit(s) retiré(s) des populaires.', messages.SUCCESS)


@admin.action(description='🆕 Marquer comme nouveau')
def marquer_nouveau(modeladmin, request, queryset):
    updated = queryset.update(nouveau=True)
    modeladmin.message_user(request, f'{updated} produit(s) marqué(s) comme nouveau.', messages.SUCCESS)


@admin.action(description='🔄 Retirer des nouveaux')
def retirer_nouveau(modeladmin, request, queryset):
    updated = queryset.update(nouveau=False)
    modeladmin.message_user(request, f'{updated} produit(s) retiré(s) des nouveaux.', messages.SUCCESS)


@admin.action(description='📦 Marquer en rupture de stock')
def marquer_rupture(modeladmin, request, queryset):
    updated = queryset.update(quantite_en_stock=0)
    modeladmin.message_user(request, f'{updated} produit(s) mis en rupture de stock.', messages.WARNING)


# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom_display', 'categorie', 'couleur', 'prix', 'quantite_en_stock', 'populaire', 'nouveau', 'image_preview')
    list_display_links = ('nom_display',)
    list_editable = ('populaire', 'nouveau', 'quantite_en_stock')
    list_filter = ('categorie', 'couleur', 'populaire', 'nouveau')
    search_fields = ('description',)
    ordering = ('-date_ajout',)
    readonly_fields = ('date_ajout', 'image_preview')
    actions = [
        marquer_populaire,
        retirer_populaire,
        marquer_nouveau,
        retirer_nouveau,
        marquer_rupture,
    ]
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'description', 'categorie', 'couleur', 'prix', 'quantite_en_stock')
        }),
        ('Images', {
            'fields': ('image', 'image_url', 'image_preview')
        }),
        ('Mise en avant', {
            'fields': ('populaire', 'nouveau', 'date_ajout')
        }),
    )

    @admin.display(description='Nom')
    def nom_display(self, obj):
        return obj.get_nom_display()

    @admin.display(description='Aperçu')
    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:4px;"/>'
                '</a>',
                url, url,
            )
        return '—'