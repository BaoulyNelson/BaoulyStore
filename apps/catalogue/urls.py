from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    # ── Homepage ──────────────────────────────────────────────────────────
    path('', views.index, name='index'),

    # ── Product listing & detail ──────────────────────────────────────────
    path('produits/', views.liste_produits, name='liste'),
    path('produits/<int:pk>/', views.detail_produit, name='detail'),
    path('categorie/<str:categorie>/', views.produits_par_categorie, name='categorie'),
    path('populaires/', views.produits_populaires, name='populaires'),
    path('nouveaux/', views.produits_nouveaux, name='nouveaux'),
    path('shop/', views.produits_nouveaux, name='shop'),   # legacy alias

    # ── Search ────────────────────────────────────────────────────────────
    path('recherche/', views.recherche_page, name='recherche'),
    path('search/', views.search_results, name='search_results'),

    # ── Staff CRUD ────────────────────────────────────────────────────────
    path('produits/ajouter/', views.add_article, name='add_article'),
    path('produits/<int:pk>/modifier/', views.edit_article, name='edit_article'),
    path('produits/<int:pk>/supprimer/', views.delete_article, name='delete_article'),
]
