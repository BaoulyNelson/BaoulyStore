from moncashify import API  # Assurez-vous que le module MonCashify est bien installé
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Panier, Commentaire,User  # Importer tous les modèles nécessaires à la fois
from .forms import CommentaireForm, ContactForm, UserRegistrationForm  # Importer tous les formulaires à la fois
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from .models import User
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.admin.sites import site


def index(request):
    # Récupère tous les commentaires triés du plus récent au plus ancien
    commentaires = Commentaire.objects.all().order_by('-date_postee')
    
    return render(request, 'index.html', {
        'commentaires': commentaires,
    })

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')

            # Authentification avec email ou nom d'utilisateur
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                # Essayons de trouver un utilisateur avec l'email
                try:
                    from django.contrib.auth.models import User
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass

            if user is not None:
                login(request, user)
                return redirect('index')  # Redirection après la connexion
            else:
                form.add_error(None, "Email/Nom d'utilisateur ou mot de passe invalide")

    return render(request, 'registration/login.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hachage du mot de passe
            user.save()

            # Connexion automatique après l'inscription
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Redirection vers un produit ou une autre page après l'inscription
            produit_id = request.POST.get('produit_id')
            if produit_id:
                return redirect('ajouter_au_panier', produit_id=produit_id)  # Si vous avez cette fonctionnalité
            return redirect('index')  # Rediriger vers la page d'accueil ou autre page
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})



def confirmer_deconnexion(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')  # Redirection après déconnexion
    return render(request, 'registration/confirmer_deconnexion.html')


def produits_par_categorie(request, categorie):
    produits = Produit.objects.filter(categorie=categorie)
    return render(request, 'liste_produits.html', {'produits': produits, 'categorie': categorie})


def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'liste_produits.html', {'produits': produits})


def detail_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    commentaires = produit.commentaires.all()  # Récupère tous les commentaires associés à ce produit

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

    return render(request, 'detail_produit.html', {
        'produit': produit,
        'commentaires': commentaires,
        'form': form  # Formulaire sera None si l'utilisateur n'est pas connecté
    })


def profile(request):
    return render(request, 'registration/profile.html')  # Assure-toi d'avoir un template 'profile.html'


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


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Traitez les données du formulaire ici
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Vous pouvez envoyer un email ou sauvegarder les informations dans une base de données
            send_mail(
                f"Message de {name}",  # Sujet
                message,  # Corps de l'email
                email,  # De l'adresse email de l'utilisateur
                ['votre-email@example.com'],  # Adresse email où envoyer le message
            )
            
            # Redirigez l'utilisateur vers une page de confirmation ou un message de succès
            return render(request, 'merci.html')

    else:
        form = ContactForm()

    
    return render(request, 'contact.html', {'form': form})



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
    return render(request, 'recherche.html')


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
    
    return render(request, 'search_results.html', {'produits': produits, 'pages': pages, 'query': query})
