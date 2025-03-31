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


def index(request):
    # Récupérer les commentaires du plus récent au plus ancien
    commentaires = Commentaire.objects.all().order_by('-date_postee')

    # Récupérer les produits et activer la pagination
    produits_list = Produit.objects.all().order_by('-id')  # Trie par le plus récent
    paginator = Paginator(produits_list, 8)  # 10 produits par page

    # Récupérer le numéro de la page depuis l'URL
    page_number = request.GET.get('page')
    # Obtenir les produits de la page
    produits = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'commentaires': commentaires,
        'produits': produits,  # Passer les produits paginés au template
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
    # Récupère tous les commentaires associés à ce produit
    commentaires = produit.commentaires.all()

    # Récupérer les produits similaires dans la même catégorie, exclure le produit actuel
    produits_similaires = Produit.objects.filter(
        categorie=produit.categorie).exclude(pk=produit.pk)

    form = None  # Initialiser le formulaire à None par défaut

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentaireForm(request.POST)
            if form.is_valid():
                commentaire = form.save(commit=False)
                # Assurez-vous que l'utilisateur soit connecté
                commentaire.utilisateur = request.user
                commentaire.produit = produit
                commentaire.save()
                # Redirige après soumission
                return redirect('detail_produit', pk=produit.pk)
        else:
            form = CommentaireForm()  # Afficher le formulaire si l'utilisateur est authentifié

    return render(request, 'produits/detail_produit.html', {
        'produit': produit,
        'commentaires': commentaires,
        'form': form,  # Formulaire sera None si l'utilisateur n'est pas connecté
        'produits_similaires': produits_similaires,  # Ajouter les produits similaires
    })


# API Pexels
API_KEY = "BfSInOJNBv93QrQU1SICt0LOoSLSERsXVU4GC6JGq9iQk7UWDD3Xm2MY"
URL = "https://api.pexels.com/v1/search"

CATEGORIES = ['homme', 'femme', 'enfant']
COULEURS = ['rouge', 'bleu', 'vert', 'noir', 'blanc', 'jaune']
VETEMENTS = [
    'tshirt', 'jeans', 'sweat', 'pantalon', 'veste', 'manteau',
    'robe', 'jupe', 'short', 'hoodie', 'pull', 'pyjama'
]


def importer_produits_pexels(request):
    """Vue pour importer des produits depuis Pexels"""

    params = {
        "query": "fashion clothing",  # Recherche d'images de mode
        "per_page": 20  # Nombre d'images à importer
    }
    headers = {"Authorization": API_KEY}
    response = requests.get(URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        for photo in data["photos"]:
            nom = random.choice(VETEMENTS)
            categorie = random.choice(CATEGORIES)
            couleur = random.choice(COULEURS)
            image_url = photo["src"]["medium"]  # URL de l'image

            # Créer un produit en base de données
            Produit.objects.create(
                nom=nom,
                description=f"Un {nom} tendance pour {categorie}.",
                categorie=categorie,
                # Prix aléatoire entre 1000 et 5000€
                prix=random.uniform(1000, 5000),
                quantite_en_stock=random.randint(1, 50),  # Stock aléatoire
                couleur=couleur,
                image_url=image_url  # On stocke l'URL dans image_url et non image !
            )
        messages.success(
            request, "Les produits ont été importés depuis Pexels avec succès.")
    else:
        messages.error(
            request, "Erreur lors de la récupération des produits depuis Pexels.")

    return redirect("liste_produits")


def ajouter_au_panier(request, produit_id):
    # Si l'utilisateur n'est pas connecté
    if not request.user.is_authenticated:
        return redirect(f'{reverse("login")}?next={request.path}')

    produit = get_object_or_404(Produit, id=produit_id)
    session_id = request.session.session_key or request.session.create()

    # Récupérer ou créer le panier pour ce produit et cette session
    panier, created = Panier.objects.get_or_create(
        produit=produit, session_id=session_id)

    if not created:
        if panier.quantite < produit.quantite_en_stock:
            panier.quantite += 1
            panier.save()
            messages.success(request, "Le produit a été ajouté au panier.")
        else:
            messages.error(request, "Stock epuisé.")
    else:
        panier.quantite = 1
        panier.save()
        messages.success(request, "Le produit a été ajouté au panier.")

    # Mettre à jour le compteur du panier dans la session
    request.session['panier_count'] = Panier.objects.filter(
        session_id=session_id).aggregate(Sum('quantite'))['quantite__sum'] or 0

    # Vérifier si la requête provient d'AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'panier_count': request.session['panier_count']})

    # Si ce n'est pas une requête AJAX, rediriger vers la page du panier
    return redirect('afficher_panier')


def afficher_panier(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    print(f"🛒 Vérification panier pour session : {session_id}")

    # Récupérer tous les articles dans le panier pour la session actuelle
    panier = Panier.objects.filter(session_id=session_id)

    # Calculer le total du panier en prenant en compte la quantité de chaque produit
    total = float(sum(item.produit.prix * item.quantite for item in panier))

    # Ajouter le total par produit dans le contexte
    for item in panier:
        item.total = item.produit.prix * item.quantite

    # Vérifier le contenu du panier
    print(f"🔍 Produits trouvés : {list(panier.values())}")

    # Sauvegarder le total dans la session pour l'utiliser ailleurs si nécessaire
    request.session['total_panier'] = total

    return render(request, 'afficher_panier.html', {
        'panier': panier,
        'total': total
    })


def modifier_quantite_panier(request, produit_id, quantite):
    produit = get_object_or_404(Produit, id=produit_id)
    session_id = request.session.session_key or request.session.create()
    panier = get_object_or_404(Panier, produit=produit, session_id=session_id)

    if quantite > 0 and quantite <= produit.quantite_en_stock:
        panier.quantite = quantite
        panier.save()
    elif quantite == 0:
        panier.delete()

    # 🔹 Mise à jour du compteur du panier
    request.session['panier_count'] = Panier.objects.filter(
        session_id=session_id).aggregate(Sum('quantite'))['quantite__sum'] or 0
    request.session.modified = True

    return redirect('afficher_panier')


def supprimer_du_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    session_id = request.session.session_key or request.session.create()

    if request.method == 'POST':
        panier = get_object_or_404(
            Panier, produit=produit, session_id=session_id)
        panier.delete()

        # 🔹 Mise à jour du compteur du panier
        request.session['panier_count'] = Panier.objects.filter(
            session_id=session_id).aggregate(Sum('quantite'))['quantite__sum'] or 0
        request.session.modified = True

        return redirect('afficher_panier')

    return render(request, 'confirmation.html', {'produit': produit})


def panier_context(request):
    session_id = request.session.session_key or request.session.create()
    panier_count = Panier.objects.filter(session_id=session_id).aggregate(
        Sum('quantite'))['quantite__sum'] or 0

    return {'panier_count': panier_count}


@login_required
def ajouter_commentaire(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.produit = produit
            commentaire.utilisateur = request.user
            commentaire.save()
            return redirect('detail_produit', pk=produit.id)

    else:
        form = CommentaireForm()

    return render(request, 'index.html', {'form': form, 'produit': produit})


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


@login_required
def custom_admin_index(request):
    context = {
        'show_dashboard_stats': True,  # Variable pour afficher le bouton
        'site_header': site.site_header,
        'site_title': site.site_title,
        'index_title': site.index_title,
    }
    return render(request, 'admin/index.html', context)


@login_required
def admin_dashboard_stats(request):
    total_utilisateurs = User.objects.count()
    total_produits = Produit.objects.count()
    total_commentaires = Commentaire.objects.count()

    context = {
        'num_users': total_utilisateurs,
        'num_produits': total_produits,
        'num_commentaires': total_commentaires,
    }
    return render(request, 'admin/admin_dashboard_stats.html', context)


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


def new_arrivals(request):
    return render(request, 'new_arrivals.html')


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
