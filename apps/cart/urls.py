from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view'),
    path('ajouter/<int:produit_id>/', views.add_to_cart, name='add'),
    path('modifier/<int:produit_id>/<int:quantite>/', views.update_quantity, name='update'),
    path('supprimer/<int:produit_id>/', views.remove_from_cart, name='remove'),
]
