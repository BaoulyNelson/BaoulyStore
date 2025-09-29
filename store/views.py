from moncashify import API
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Panier, Commentaire, User
from .forms import CommentaireForm, ContactForm, ProfileForm, ProduitForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import User
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.admin.sites import site
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.db.models import Sum
# Importation de la fonction reverse
from django.urls import reverse
import requests
import random
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.conf import settings
from moncashify import API
from .models import Panier
from django.views.decorators.http import require_POST




def index(request):
    commentaires = Commentaire.objects.all().order_by('-date')
    produits_list = Produit.objects.all().order_by('-id')
    paginator = Paginator(produits_list, 12)
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)

    # spécifiques
    nouveaux = Produit.objects.filter(nouveau=True).order_by('-id')[:9]
    populaires = Produit.objects.filter(populaire=True).order_by('-id')[:9]

    return render(request, 'index.html', {
        'commentaires': commentaires,
        'produits': produits,
        'nouveaux': nouveaux,
        'populaires': populaires,
    })


def login_view(request):
    # Supprime les anciens messages avant d'afficher un nouveau
    storage = get_messages(request)
    for _ in storage:
        pass  # Cette boucle vide supprime tous les anciens messages

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Bienvenue {username} ! 😊 Vous êtes connecté.")

                if request.POST.get("remember_me"):
                    request.session.set_expiry(1209600)  # 2 semaines

                # Vérifier si un paramètre 'next' est présent dans l'URL
                # 'profile' est l'URL par défaut (peut être modifié)
                next_url = request.GET.get("next", "profile")

                return redirect(next_url)
            else:
                messages.error(
                    request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez vérifier vos informations.")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Inscription réussie ! 🎉 Bienvenue sur notre plateforme.")
            return redirect("index")  # Redirection après succès
        else:
            messages.error(
                request, "Une erreur est survenue lors de l'inscription. Vérifiez les informations.")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Redirection après la mise à jour du profil
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'registration/edit_profile.html', {'form': form})


def confirmer_deconnexion(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')  # Redirection après déconnexion
    return render(request, 'registration/confirmer_deconnexion.html')


@login_required
def add_article(request):
    if request.user.is_staff:  # Vérifiez si l'utilisateur est un membre du personnel
        if request.method == 'POST':
            # Utilisez ProduitForm pour le formulaire produit
            form = ProduitForm(request.POST, request.FILES)
            if form.is_valid():
                produit = form.save(commit=False)
                produit.save()  # Sauvegarde le produit
                messages.success(
                    request, "Le produit a été ajouté avec succès.")

                # Vérifie quel bouton a été cliqué pour rediriger
                if 'save_and_add_another' in request.POST:
                    # Redirige vers un formulaire vide pour ajouter un autre produit
                    return redirect('add_article')
                elif 'save_and_continue_editing' in request.POST:
                    # Redirige vers la page d'édition du produit
                    return redirect('edit_product', pk=produit.pk)
                else:
                    # Redirige vers la liste des produits
                    return redirect('liste_produits')
        else:
            form = ProduitForm()
        return render(request, 'produits/add_article.html', {'form': form})
    else:
        # Affiche une erreur 403 si l'utilisateur n'est pas staff
        return render(request, '403.html', status=403)


def produits_par_categorie(request, categorie):
    produits_list = Produit.objects.filter(
        categorie=categorie).order_by('-id')  # Trier par le plus récent

    # 📌 PAGINATION : 9 produits par page
    paginator = Paginator(produits_list, 12)
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)

    return render(request, 'produits/liste_produits.html', {
        'produits': produits,
        'categorie': categorie,  # Pour afficher la catégorie sélectionnée
    })


def liste_produits(request):
    # Récupérer la catégorie depuis l'URL
    categorie = request.GET.get('categorie', None)

    if categorie:
        produits_list = Produit.objects.filter(
            categorie=categorie).order_by('-id')  # Filtrer par catégorie
    else:
        produits_list = Produit.objects.all().order_by('-id')  # Tous les produits

    paginator = Paginator(produits_list, 20)  # 9 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)

    return render(request, 'produits/liste_produits.html', {
        'produits': produits,
        'categorie_actuelle': categorie,  # Pour afficher la catégorie sélectionnée
    })


def detail_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)

    # Récupérer les produits similaires dans la même catégorie, exclure le produit actuel
    produits_similaires = Produit.objects.filter(
        categorie=produit.categorie).exclude(pk=produit.pk)

    return render(request, 'produits/detail_produit.html', {
        'produit': produit,
        'produits_similaires': produits_similaires,
    })




def ajouter_au_panier(request, produit_id):
    # Si l'utilisateur n'est pas connecté
    if not request.user.is_authenticated:
        return redirect(f'{reverse("login")}?next={request.path}')

    produit = get_object_or_404(Produit, id=produit_id)

    # ✅ Assurer une session valide
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key  # toujours disponible

    # ✅ Récupérer ou créer le panier
    panier, created = Panier.objects.get_or_create(
        produit=produit,
        session_id=session_id
    )

    if not created:
        if panier.quantite < produit.quantite_en_stock:
            panier.quantite += 1
            panier.save()
            messages.success(request, "Le produit a été ajouté au panier.")
        else:
            messages.error(request, "Stock épuisé.")
    else:
        panier.quantite = 1
        panier.save()
        messages.success(request, "Le produit a été ajouté au panier.")

    # ✅ Mise à jour du compteur
    request.session['panier_count'] = (
        Panier.objects.filter(session_id=session_id)
        .aggregate(Sum('quantite'))['quantite__sum'] or 0
    )

    # ✅ Réponse AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'panier_count': request.session['panier_count']})

    return redirect('afficher_panier')




def afficher_panier(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
    session_id = request.session.session_key

    panier = Panier.objects.filter(session_id=session_id)
    total = float(sum(item.produit.prix * item.quantite for item in panier))

    for item in panier:
        item.total = item.produit.prix * item.quantite

    request.session['total_panier'] = total

    payment_url = None
    error_message = None

    if total > 0:
        try:
            moncash_api = API(
                client_id=settings.MONCASH_CLIENT_ID,
                secret_key=settings.MONCASH_SECRET_ID,
                debug=settings.MONCASH_DEBUG
            )

            # Crée un paiement MonCash
            payment = moncash_api.payment(
                order_id=f"order-{session_id}",  # L'ID de commande unique
                amount=total  # Le montant total du panier
            )

        
            payment_url = payment.redirect_url  # ✅ accès direct à l'attribut


        except Exception as e:
            error_message = f"Erreur Moncash : {str(e)}"

    else:
        error_message = "Le panier est vide."

    return render(request, 'panier/afficher_panier.html', {
        'panier': panier,
        'total': total,
        'payment_url': payment_url,
        'error_message': error_message
        
    })



def modifier_quantite(request, produit_id, quantite):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
    session_id = request.session.session_key

    panier_item = Panier.objects.get(session_id=session_id, produit_id=produit_id)

    if request.method == "POST":
        # ⚡ on prend la quantité depuis l'URL
        panier_item.quantite = quantite
        panier_item.save()

    # Recalcul total backend
    panier = Panier.objects.filter(session_id=session_id)
    total = sum(item.produit.prix * item.quantite for item in panier)
    request.session["total_panier"] = float(total)

    # Générer une nouvelle payment_url
    # payment_url = None
    # if total > 0:
    #     try:
    #         moncash_api = API(
    #             client_id=settings.MONCASH_CLIENT_ID,
    #             secret_key=settings.MONCASH_SECRET_ID,
    #             debug=settings.MONCASH_DEBUG
    #         )
    #         payment = moncash_api.payment(
    #             order_id=f"order-{session_id}",
    #             amount=total
    #         )
    #         payment_url = payment.redirect_url
    #     except Exception:
    #         pass
    # print(total)
    # print(payment_url)
    payment_url = None
    if total > 0:
        try:
            moncash_api = API(
                client_id=settings.MONCASH_CLIENT_ID,
                secret_key=settings.MONCASH_SECRET_ID,
                debug=settings.MONCASH_DEBUG
            )
            total_float = float(total)  # ← convertir en float
            payment = moncash_api.payment(
                order_id=f"order-{session_id}",
                amount=total_float
            )
            payment_url = payment.redirect_url
        except Exception as e:
            print("Erreur MonCash:", e)



    return JsonResponse({
        "item_total": float(panier_item.produit.prix * panier_item.quantite),
        "total": float(total),
        "panier_count": panier.count(),
        "payment_url": payment_url,
    })



from django.views.decorators.http import require_POST

def supprimer_du_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key  

    if request.method == "POST":
        try:
            panier = Panier.objects.get(produit=produit, session_id=session_id)
            panier.delete()
        except Panier.DoesNotExist:
            messages.error(request, "Ce produit n'est plus dans votre panier.")
            return redirect("afficher_panier")

        # 🔹 Mise à jour du compteur
        request.session['panier_count'] = (
            Panier.objects.filter(session_id=session_id)
            .aggregate(Sum('quantite'))['quantite__sum'] or 0
        )
        request.session.modified = True

        messages.success(request, f"{produit.nom} a été supprimé du panier.")
        return redirect("afficher_panier")

    # 🔹 Si GET → afficher confirmation
    return render(request, "panier/confirmation.html", {"produit": produit})






def ajouter_commentaire(request):
    if request.method == "POST":
        form = CommentaireForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("index")  # redirige vers la page d’accueil ou une autre
    else:
        form = CommentaireForm()

    return render(request, "commentaires/ajouter_commentaire.html", {"form": form})


# Vue pour supprimer un commentaire, réservée aux superusers
@user_passes_test(lambda u: u.is_superuser)
def supprimer_commentaire(request, commentaire_id):
    commentaire = get_object_or_404(Commentaire, id=commentaire_id)
    # Récupère l'ID du produit avant la suppression
    produit_id = commentaire.produit.pk
    commentaire.delete()
    return redirect('index')  # Redirige correctement avec 'pk'


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            # 📩 Envoyer un email (assure-toi que les paramètres SMTP sont bien configurés)
            send_mail(
                subject=f"Nouveau message de {name}",
                message=message,
                from_email=email,
                recipient_list=["elconquistadorbaoulyn@example.com"],  #
                fail_silently=False,
            )

            messages.success(request, "Votre message a bien été envoyé !")
            # Redirige vers la page de succès
            return redirect("contact_success")

    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})


def contact_success_view(request):
    return render(request, "contact/contact_success.html")


def recherche_page(request):
    return render(request, 'search/recherche.html')


def search_results(request):
    query = request.GET.get('q')
    # Recherche les produits par nom
    produits = Produit.objects.filter(nom__icontains=query)

    # Recherche pour les pages spécifiques en fonction de la requête
    pages = []

    if 'accueil' in query.lower():
        pages.append({'nom': 'Accueil', 'url': 'accueil'})

    if 'produits' in query.lower():
        pages.append({'nom': 'Produits', 'url': 'liste_produits'})

    if 'femme' in query.lower():
        pages.append(
            {'nom': 'Femme', 'url': 'produits_par_categorie', 'categorie': 'femme'})

    if 'homme' in query.lower():
        pages.append(
            {'nom': 'Homme', 'url': 'produits_par_categorie', 'categorie': 'homme'})

    if 'enfant' in query.lower():
        pages.append(
            {'nom': 'Enfant', 'url': 'produits_par_categorie', 'categorie': 'enfant'})

    if 'contact' in query.lower():
        pages.append({'nom': 'Contact', 'url': 'contact'})

    return render(request, 'search/search_results.html', {'produits': produits, 'pages': pages, 'query': query})




def produits_populaires(request):
    populaires = Produit.objects.filter(populaire=True).order_by('-id')[:20]  # Limiter à 20 produits populaires
    return render(request, 'produits/produits_populaires.html', {'populaires': populaires})


def produits_nouveaux(request):
    nouveaux = Produit.objects.filter(nouveau=True).order_by('-id')[:20]  # Limiter à 20 produits nouveaux
    return render(request, 'produits/produits_nouveaux.html', {'nouveaux': nouveaux})

def promotions(request):
    return render(request, 'promotions.html')


def blog(request):
    return render(request, 'blog.html')


def faq(request):
    return render(request, 'faq.html')


def return_policy(request):
    return render(request, 'return_policy.html')


def order_tracking(request):
    return render(request, 'order_tracking.html')


def about(request):
    return render(request, 'about.html')



