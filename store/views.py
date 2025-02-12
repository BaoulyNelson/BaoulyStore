from moncashify import API  
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Panier, Commentaire,User
from .forms import CommentaireForm, ContactForm,ProfileForm,ProduitForm 
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
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator


def index(request):
    # Récupérer les commentaires du plus récent au plus ancien
    commentaires = Commentaire.objects.all().order_by('-date_postee')
    
    # Récupérer les produits et activer la pagination
    produits_list = Produit.objects.all().order_by('-id')  # Trie par le plus récent
    paginator = Paginator(produits_list, 8)  # 10 produits par page

    page_number = request.GET.get('page')  # Récupérer le numéro de la page depuis l'URL
    produits = paginator.get_page(page_number)  # Obtenir les produits de la page

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
                messages.success(request, f"Bienvenue {username} ! 😊 Vous êtes connecté.")

                if request.POST.get("remember_me"):
                    request.session.set_expiry(1209600)  # 2 semaines

                return redirect("profile")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
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
            messages.success(request, "Inscription réussie ! 🎉 Bienvenue sur notre plateforme.")
            return redirect("index")  # Redirection après succès
        else:
            messages.error(request, "Une erreur est survenue lors de l'inscription. Vérifiez les informations.")
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
            return redirect('profile')  # Redirection après la mise à jour du profil
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
            form = ProduitForm(request.POST, request.FILES)  # Utilisez ProduitForm pour le formulaire produit
            if form.is_valid():
                produit = form.save(commit=False)
                produit.save()  # Sauvegarde le produit
                messages.success(request, "Le produit a été ajouté avec succès.")

                # Vérifie quel bouton a été cliqué pour rediriger
                if 'save_and_add_another' in request.POST:
                    return redirect('add_article')  # Redirige vers un formulaire vide pour ajouter un autre produit
                elif 'save_and_continue_editing' in request.POST:
                    return redirect('edit_product', pk=produit.pk)  # Redirige vers la page d'édition du produit
                else:
                    return redirect('liste_produits')  # Redirige vers la liste des produits
        else:
            form = ProduitForm()
        return render(request, 'produits/add_article.html', {'form': form})
    else:
        return render(request, '403.html', status=403)  # Affiche une erreur 403 si l'utilisateur n'est pas staff
    



def produits_par_categorie(request, categorie):
    produits_list = Produit.objects.filter(categorie=categorie).order_by('-id')  # Trier par le plus récent

    # 📌 PAGINATION : 9 produits par page
    paginator = Paginator(produits_list, 4)  
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)

    return render(request, 'produits/liste_produits.html', {
        'produits': produits,
        'categorie': categorie,  # Pour afficher la catégorie sélectionnée
    })





def liste_produits(request):
    categorie = request.GET.get('categorie', None)  # Récupérer la catégorie depuis l'URL
    
    if categorie:
        produits_list = Produit.objects.filter(categorie=categorie).order_by('-id')  # Filtrer par catégorie
    else:
        produits_list = Produit.objects.all().order_by('-id')  # Tous les produits

    paginator = Paginator(produits_list, 8)  # 9 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)

    return render(request, 'produits/liste_produits.html', {
        'produits': produits,
        'categorie_actuelle': categorie,  # Pour afficher la catégorie sélectionnée
    })






def detail_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    commentaires = produit.commentaires.all()  # Récupère tous les commentaires associés à ce produit

    # Récupérer les produits similaires dans la même catégorie, exclure le produit actuel
    produits_similaires = Produit.objects.filter(categorie=produit.categorie).exclude(pk=produit.pk)

    form = None  # Initialiser le formulaire à None par défaut

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentaireForm(request.POST)
            if form.is_valid():
                commentaire = form.save(commit=False)
                commentaire.utilisateur = request.user  # Assurez-vous que l'utilisateur soit connecté
                commentaire.produit = produit
                commentaire.save()
                return redirect('detail_produit', pk=produit.pk)  # Redirige après soumission
        else:
            form = CommentaireForm()  # Afficher le formulaire si l'utilisateur est authentifié

    return render(request, 'produits/detail_produit.html', {
        'produit': produit,
        'commentaires': commentaires,
        'form': form,  # Formulaire sera None si l'utilisateur n'est pas connecté
        'produits_similaires': produits_similaires,  # Ajouter les produits similaires
    })



def ajouter_au_panier(request, produit_id):
    # Si l'utilisateur n'est pas connecté, envoyer une réponse JSON avec un statut d'erreur
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'not_logged_in'})

    # Si l'utilisateur est connecté, continuer avec le processus d'ajout au panier
    produit = get_object_or_404(Produit, id=produit_id)
    session_id = request.session.session_key or request.session.create()

    # Récupérer ou créer le panier pour ce produit et cette session
    panier, created = Panier.objects.get_or_create(produit=produit, session_id=session_id)

    # Quantité actuelle dans le panier
    quantite_actuelle = panier.quantite

    if not created:
        if quantite_actuelle < produit.quantite_en_stock:
            panier.quantite += 1
            panier.save()
            messages.success(request, "Le produit a été ajouté au panier.")
        else:
            messages.error(request, "Quantité maximale atteinte. Le stock est insuffisant pour ajouter plus de ce produit.")
    else:
        panier.quantite = 1
        panier.save()
        messages.success(request, "Le produit a été ajouté au panier.")
    
    return JsonResponse({'status': 'success'})




def afficher_panier(request):
    # Vérifier ou créer une session
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    # Récupérer les articles du panier
    panier = Panier.objects.filter(session_id=session_id)
    total = float(sum(item.produit.prix * item.quantite for item in panier))

    # Stocker le total dans la session
    request.session['total_panier'] = total

    # Initialisation de l'API MonCash avec les informations sécurisées
    client_id = settings.MONCASH_CLIENT_ID
    secret_id = settings.MONCASH_SECRET_ID
    debug = settings.MONCASH_DEBUG

    # Initialiser MonCash API
    moncash = API(client_id, secret_id, debug)
    order_id = 'Baouly Store'  # Vous pouvez personnaliser cet ID
    price = request.session['total_panier']
    
    try:
        # Création du paiement avec le montant total du panier
        payment = moncash.payment(order_id, price)
        
        # Vérifiez si la réponse de l'API est valide et contient une URL de redirection
        if not hasattr(payment, 'redirect_url'):
            raise Exception("Erreur lors de la génération de l'URL de paiement.")

        # Passer l'URL de redirection au template
        payment_url = payment.redirect_url

    except Exception as e:
        # Gérer les erreurs et les afficher
        payment_url = ''
        error_message = f"Erreur lors de la création du paiement : {str(e)}"
        return render(request, 'afficher_panier.html', {
            'panier': panier, 
            'total': total, 
            'payment_url': payment_url, 
            'error_message': error_message
        })

    # Passer l'URL de redirection au template
    return render(request, 'afficher_panier.html', {
        'panier': panier, 
        'total': total, 
        'payment_url': payment_url
    })



def modifier_quantite_panier(request, produit_id, quantite):
    produit = get_object_or_404(Produit, id=produit_id)
    session_id = request.session.session_key
    panier = get_object_or_404(Panier, produit=produit, session_id=session_id)
    
    if quantite > 0 and quantite <= produit.quantite_en_stock:
        # Mettre à jour la quantité dans le panier
        panier.quantite = quantite
        panier.save()
    elif quantite == 0:
        # Supprimer l'élément du panier si la quantité est 0
        panier.delete()
    
    return redirect('afficher_panier')


def supprimer_du_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    session_id = request.session.session_key

    if request.method == 'POST':
        # Supprimer l'article du panier si la méthode est POST (après confirmation)
        panier = get_object_or_404(Panier, produit=produit, session_id=session_id)
        panier.delete()
        return redirect('afficher_panier')
    
    # Si la méthode est GET, afficher une page de confirmation
    return render(request, 'confirmation.html', {'produit': produit})


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
    produit_id = commentaire.produit.pk  # Récupère l'ID du produit avant la suppression
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
            return redirect("contact_success")  # Redirige vers la page de succès

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
    produits = Produit.objects.filter(nom__icontains=query)  # Recherche les produits par nom

    # Recherche pour les pages spécifiques en fonction de la requête
    pages = []
    
    if 'accueil' in query.lower():
        pages.append({'nom': 'Accueil', 'url': 'accueil'})
    
    if 'produits' in query.lower():
        pages.append({'nom': 'Produits', 'url': 'liste_produits'})
    
    if 'femme' in query.lower():
        pages.append({'nom': 'Femme', 'url': 'produits_par_categorie', 'categorie': 'femme'})
    
    if 'homme' in query.lower():
        pages.append({'nom': 'Homme', 'url': 'produits_par_categorie', 'categorie': 'homme'})
    
    if 'enfant' in query.lower():
        pages.append({'nom': 'Enfant', 'url': 'produits_par_categorie', 'categorie': 'enfant'})
    
    if 'contact' in query.lower():
        pages.append({'nom': 'Contact', 'url': 'contact'})
    
    return render(request, 'search/search_results.html', {'produits': produits, 'pages': pages, 'query': query})
