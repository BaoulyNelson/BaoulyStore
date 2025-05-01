from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import Produit, Commentaire
from django.utils.safestring import mark_safe


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

admin_site = MyAdminSite(name='myadmin')

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix', 'image_display')

    def image_display(self, obj):
        if obj.image_url:  # ✅ Utilise le champ `image_url` pour les images distantes
            return mark_safe(f'<img src="{obj.image_url}" width="50" height="50" />')
        elif obj.image:  # ✅ Utilise `image.url` pour les images locales
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "Pas d'image"

    image_display.short_description = "Aperçu"

admin.site.register(Produit, ProduitAdmin)

# 📌 Enregistrer correctement les modèles dans `admin_site` au lieu de `admin`
admin_site.register(User)
admin_site.register(Group)
admin_site.register(Produit, ProduitAdmin)  # ✅ Corrigé ici
admin_site.register(Commentaire)
 