from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
from .models import Produit, Commentaire

from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.urls import path
from .models import Produit, Commentaire

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
        # Votre logique pour récupérer les statistiques
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

admin_site.register(User)
admin_site.register(Group)
admin_site.register(Produit)
admin_site.register(Commentaire)
