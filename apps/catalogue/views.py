"""
Catalogue views — product listing, detail, search, and staff CRUD.
All business logic delegates to catalogue.services.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from apps.reviews.models import Commentaire
from .forms import ProduitForm
from .models import Produit
from . import services


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

def index(request):
    """Homepage: paginated product list + featured sections."""
    produits = services.get_produits_page(
        page_number=request.GET.get('page'),
        per_page=102,
    )
    context = {
        'produits': produits,
        'nouveaux': services.get_produits_nouveaux(limit=9),
        'populaires': services.get_produits_populaires(limit=9),
        'commentaires': Commentaire.objects.order_by('-date')[:10],
    }
    return render(request, 'catalogue/index.html', context)


def liste_produits(request):
    """Paginated product list, optionally filtered by category."""
    categorie = request.GET.get('categorie') or None
    produits = services.get_produits_page(
        categorie=categorie,
        page_number=request.GET.get('page'),
    )
    return render(request, 'catalogue/liste_produits.html', {
        'produits': produits,
        'categorie_actuelle': categorie,
    })


def produits_par_categorie(request, categorie):
    """Legacy URL — delegates to liste_produits logic."""
    produits = services.get_produits_page(
        categorie=categorie,
        page_number=request.GET.get('page'),
    )
    return render(request, 'catalogue/liste_produits.html', {
        'produits': produits,
        'categorie_actuelle': categorie,
    })


def detail_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    return render(request, 'catalogue/detail_produit.html', {
        'produit': produit,
        'produits_similaires': services.get_produits_similaires(produit),
    })


def produits_populaires(request):
    populaires = services.get_produits_populaires(limit=100)
    return render(request, 'catalogue/produits_populaires.html', {'populaires': populaires})


def produits_nouveaux(request):
    nouveaux = services.get_produits_nouveaux(limit=100)
    return render(request, 'catalogue/produits_nouveaux.html', {'nouveaux': nouveaux})


def search_results(request):
    query = request.GET.get('q', '').strip()
    produits = services.search_produits(query) if query else Produit.objects.none()

    # Simple page-route suggestions based on keywords
    pages = []
    ql = query.lower()
    routes = [
        ('accueil',  'Accueil',   'catalogue:index',    None),
        ('produits', 'Produits',  'catalogue:liste',    None),
        ('femme',    'Femme',     'catalogue:categorie', 'femme'),
        ('homme',    'Homme',     'catalogue:categorie', 'homme'),
        ('enfant',   'Enfant',    'catalogue:categorie', 'enfant'),
        ('contact',  'Contact',   'pages:contact',      None),
    ]
    for keyword, nom, url, cat in routes:
        if keyword in ql:
            entry = {'nom': nom, 'url': url}
            if cat:
                entry['categorie'] = cat
            pages.append(entry)

    return render(request, 'catalogue/search_results.html', {
        'produits': produits,
        'pages': pages,
        'query': query,
    })


def recherche_page(request):
    return render(request, 'catalogue/recherche.html')


# ---------------------------------------------------------------------------
# Staff-only CRUD views
# ---------------------------------------------------------------------------

def _is_staff(user):
    return user.is_active and user.is_staff


@login_required
@user_passes_test(_is_staff, login_url='catalogue:index')
def add_article(request):
    form = ProduitForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        produit = form.save()
        messages.success(request, "Le produit a été ajouté avec succès.")
        if 'save_and_add_another' in request.POST:
            return redirect('catalogue:add_article')
        if 'save_and_continue_editing' in request.POST:
            return redirect('catalogue:edit_article', pk=produit.pk)
        return redirect('catalogue:liste')
    return render(request, 'catalogue/add_article.html', {'form': form})


@login_required
@user_passes_test(_is_staff, login_url='catalogue:index')
def edit_article(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    form = ProduitForm(request.POST or None, request.FILES or None, instance=produit)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Le produit a été mis à jour.")
        return redirect('catalogue:detail', pk=produit.pk)
    return render(request, 'catalogue/edit_article.html', {'form': form, 'produit': produit})


@login_required
@user_passes_test(_is_staff, login_url='catalogue:index')
def delete_article(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, "Le produit a été supprimé.")
        return redirect('catalogue:liste')
    return render(request, 'catalogue/confirm_delete.html', {'produit': produit})
