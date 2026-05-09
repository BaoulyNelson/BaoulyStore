from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import CommentaireForm

def ajouter_commentaire(request):
    form = CommentaireForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Merci pour votre témoignage !")
        return redirect('catalogue:index')
    return render(request, 'reviews/ajouter_commentaire.html', {'form': form})
