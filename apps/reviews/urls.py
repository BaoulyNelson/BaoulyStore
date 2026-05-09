from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('ajouter/', views.ajouter_commentaire, name='ajouter'),
]
