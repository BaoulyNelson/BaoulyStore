from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Connexion utilisateur
    path('login/', views.login_view, name='login'),

    # Inscription utilisateur
    path('signup/', views.signup_view, name='signup'),

    # Déconnexion utilisateur puis redirection vers l’accueil
    path('logout/', auth_views.LogoutView.as_view(next_page='catalogue:index'), name='logout'),

    # Page de confirmation avant déconnexion
    path('confirmer-deconnexion/', views.confirmer_deconnexion, name='confirmer_deconnexion'),

    # Affichage du profil utilisateur connecté
    path('profil/', views.profile_view, name='profile'),

    # Modification des informations du profil
    path('profil/modifier/', views.edit_profile, name='edit_profile'),

    # Changement du mot de passe utilisateur
    path('profil/mot-de-passe/', views.change_password, name='change_password'),

    # Formulaire de demande de réinitialisation du mot de passe par email
    path('mot-de-passe/reinitialiser/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html', email_template_name='accounts/password_reset_email.html', subject_template_name='accounts/password_reset_subject.txt'), name='password_reset'),

    # Page affichée après envoi du mail de réinitialisation
    path('mot-de-passe/reinitialiser/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    # Validation du lien reçu par email + définition du nouveau mot de passe
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),

    # Confirmation finale du changement de mot de passe
    path('reinitialiser/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]