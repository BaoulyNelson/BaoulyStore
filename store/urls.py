# store/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import login_view,register,confirmer_deconnexion,produits_par_categorie,recherche_page,supprimer_commentaire,admin_dashboard_stats,ajouter_commentaire,custom_admin_index

urlpatterns = [
    path('', views.index, name='index'),  # Page d'accueil
    path('categorie/<str:categorie>/', produits_par_categorie, name='produits_par_categorie'),
    path('contact/', views.contact, name='contact'),
    path('liste_produits/', views.liste_produits, name='liste_produits'),
    path('ajouter-article/', views.add_article, name='add_article'),
    path('detail_produit/<int:pk>/', views.detail_produit, name='detail_produit'),
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.afficher_panier, name='afficher_panier'),
    path('modifier-quantite/<int:produit_id>/<int:quantite>/', views.modifier_quantite_panier, name='modifier_quantite_panier'),
    path('supprimer-du-panier/<int:produit_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('search/', views.search_results, name='search_results'),
    path('recherche/', recherche_page, name='recherche'),  # URL pour afficher recherche.html
    
   
    path('admin/stats/', admin_dashboard_stats, name='admin_dashboard_stats'),  # Statistiques
  
    path('admin/', custom_admin_index, name='admin_index'),  

   path('login/', login_view, name='login'),  # Vue de connexion personnalisée
    path('register/', register, name='register'),  # Vue d'inscription
    path('profile/', views.profile_view, name='profile'),
    
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('confirmer-deconnexion/', confirmer_deconnexion, name='confirmer_deconnexion'),
    path('ajouter_commentaire/<int:produit_id>/', ajouter_commentaire, name='ajouter_commentaire'),
 
    path('supprimer_commentaire/<int:commentaire_id>/', supprimer_commentaire, name='supprimer_commentaire'),

]
