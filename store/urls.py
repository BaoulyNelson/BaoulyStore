# store/urls.py

# Importation des vues et des modules nécessaires
from django.urls import path
from . import views  # Importation des vues locales
from django.contrib.auth import views as auth_views  # Importation des vues par défaut pour la gestion des utilisateurs
from .views import login_view, signup_view, confirmer_deconnexion, produits_par_categorie, recherche_page, supprimer_commentaire, admin_dashboard_stats, ajouter_commentaire, custom_admin_index

urlpatterns = [
    # Page d'accueil du site
    path('', views.index, name='index'),

    # URL pour afficher les produits par catégorie
    path('categorie/<str:categorie>/', produits_par_categorie, name='produits_par_categorie'),

    # Page de contact du site
    path("contact/",views.contact_view, name="contact"),
    # Page Témoignages
    path("contact/success/", views.contact_success_view, name="contact_success"),

    # Liste des produits
    path('liste_produits/', views.liste_produits, name='liste_produits'),

    # Ajouter un article
    path('ajouter-article/', views.add_article, name='add_article'),

    # Détail d'un produit spécifique
    path('detail_produit/<int:pk>/', views.detail_produit, name='detail_produit'),

    # Ajouter un produit au panier
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),

    # Afficher le panier
    path('panier/', views.afficher_panier, name='afficher_panier'),

    # Modifier la quantité d'un produit dans le panier
    path('modifier-quantite/<int:produit_id>/<int:quantite>/', views.modifier_quantite_panier, name='modifier_quantite_panier'),

    # Supprimer un produit du panier
    path('supprimer-du-panier/<int:produit_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),

    # Résultats de recherche
    path('search/', views.search_results, name='search_results'),

    # Page de recherche avec un formulaire de recherche
    path('recherche/', recherche_page, name='recherche'),  # URL pour afficher recherche.html

    # Statistiques de l'admin
    path('admin/stats/', admin_dashboard_stats, name='admin_dashboard_stats'),

    # Vue personnalisée pour l'index de l'admin
    path('admin/', custom_admin_index, name='admin_index'),

    # Page de connexion (vue personnalisée)
    path('login/', login_view, name='login'),

    # Page d'inscription (vue personnalisée)
    path('signup/', views.signup_view, name='signup'),
  
    # Vue du profil utilisateur
    path('profile/', views.profile_view, name='profile'),

    # Changer de mot de passe
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Réinitialisation du mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    # Confirmation de réinitialisation de mot de passe
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # Page de confirmation après la réinitialisation du mot de passe
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Page d'édition du profil utilisateur
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Confirmation avant de se déconnecter
    path('confirmer-deconnexion/', confirmer_deconnexion, name='confirmer_deconnexion'),

    # Ajouter un commentaire à un produit
    path('ajouter_commentaire/<int:produit_id>/', ajouter_commentaire, name='ajouter_commentaire'),

    # Supprimer un commentaire d'un produit
    path('supprimer_commentaire/<int:commentaire_id>/', supprimer_commentaire, name='supprimer_commentaire'),
]
