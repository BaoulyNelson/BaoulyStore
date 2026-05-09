from django import forms
from .models import Commentaire

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['nom', 'photo', 'texte', 'role']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Client fidèle'}),
            'texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Votre témoignage'}),
        }
