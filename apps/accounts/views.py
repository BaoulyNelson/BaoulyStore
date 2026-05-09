"""
Accounts views — login, signup, profile, logout confirmation.
Password reset delegates to Django's built-in views (configured in urls.py).
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.messages import get_messages
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import ProfileForm


def login_view(request):
    # Flush stale flash messages before showing the login page
    list(get_messages(request))

    if request.user.is_authenticated:
        return redirect('catalogue:index')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.POST.get('remember_me'):
                request.session.set_expiry(1_209_600)  # 2 weeks
            messages.success(request, f"Bienvenue {user.get_short_name() or user.username} !")
            return redirect(request.GET.get('next') or 'catalogue:index')
        messages.error(request, "Identifiant ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})




def signup_view(request):
    if request.user.is_authenticated:
        return redirect('catalogue:index')

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # multi-backend fix
            user.backend = 'apps.accounts.backends.EmailOrUsernameBackend'
            login(request, user)

            messages.success(request, "Inscription réussie ! Bienvenue sur Baouly's Store.")

            # 🔥 SAFE REDIRECT
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)

            return redirect('catalogue:index')

        messages.error(request, "Veuillez corriger les erreurs ci-dessous.")

    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {
        'form': form,
        'next': next_url or ''
    })

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm, CustomPasswordChangeForm

@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('accounts:profile')
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    form = CustomPasswordChangeForm(user=request.user, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)  # ← garde la session active
        messages.success(request, "Mot de passe modifié avec succès.")
        return redirect('accounts:profile')
    return render(request, 'accounts/edit_profile.html', {
        'form': ProfileForm(instance=request.user),  # ← profil intact
        'password_form': form,
    })


def confirmer_deconnexion(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Vous avez été déconnecté.")
        return redirect('catalogue:index')
    return render(request, 'accounts/confirmer_deconnexion.html')
