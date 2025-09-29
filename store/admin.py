from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import Produit, Commentaire
from django.utils.html import mark_safe


class MyAdminSite(admin.AdminSite):
    site_header = 'BaoulyStore Administration'
    site_title = 'BaoulyStore Admin'
    index_title = 'Bienvenue dans votre tableau de bord'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stats/', self.admin_view(self.admin_dashboard_stats), name='admin_dashboard_stats'),
        ]
        return custom_urls + urls

    def admin_dashboard_stats(self, request):
        total_utilisateurs = User.objects.count()
        total_produits = Produit.objects.count()
        total_commentaires = Commentaire.objects.count()
        context = {
            'num_users': total_utilisateurs,
            'num_produits': total_produits,
            'num_commentaires': total_commentaires,
        }
        return render(request, 'admin/admin_dashboard_stats.html', context)


# ✅ Créer ton site admin personnalisé
admin_site = MyAdminSite(name='myadmin')


# --- Admin Produit ---
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'image_display')

    def image_display(self, obj):
        if obj.get_image():  # suppose que ton modèle a une méthode get_image()
            return mark_safe(f'<img src="{obj.get_image()}" width="50" height="50" />')
        return "Pas d'image"

    image_display.short_description = "Aperçu"


# --- Admin Commentaire ---
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ("nom", "role", "date", "aperçu_texte")
    search_fields = ("nom", "texte", "role")
    list_filter = ("role", "date")
    ordering = ("-date",)

    def aperçu_texte(self, obj):
        return obj.texte[:50] + ("..." if len(obj.texte) > 50 else "")
    aperçu_texte.short_description = "Aperçu du commentaire"


# ✅ Enregistrer tout sur admin_site
admin_site.register(User)
admin_site.register(Group)
admin_site.register(Produit, ProduitAdmin)
admin_site.register(Commentaire, CommentaireAdmin)
