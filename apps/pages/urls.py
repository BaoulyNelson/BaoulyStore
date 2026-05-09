from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('contact/merci/', views.contact_success_view, name='contact_success'),
    path('promotions/', views.promotions, name='promotions'),
    path('blog/', views.blog, name='blog'),
    path('faq/', views.faq, name='faq'),
    path('politique-retour/', views.return_policy, name='return_policy'),
    path('suivi-commande/', views.order_tracking, name='order_tracking'),
    path('a-propos/', views.about, name='about'),
]
