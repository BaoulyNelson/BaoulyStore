from django import forms
from .models import Produit


class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = [
            'nom', 'description', 'categorie',
            'prix', 'quantite_en_stock', 'image',
            'image_url', 'couleur', 'populaire', 'nouveau',
        ]
        labels = {
            'nom': 'Type de vêtement',
            'description': 'Description',
            'categorie': 'Catégorie',
            'prix': 'Prix (HTG)',
            'quantite_en_stock': 'Quantité en stock',
            'image': 'Image locale',
            'image_url': 'URL image externe (Google Drive…)',
            'couleur': 'Couleur',
            'populaire': 'Marquer comme populaire',
            'nouveau': 'Marquer comme nouveau',
        }
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Jean slim noir',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez les caractéristiques du produit…',
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-select',
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00',
            }),
            'quantite_en_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://drive.google.com/…',
            }),
            'couleur': forms.Select(attrs={
                'class': 'form-select',
            }),
            'populaire': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'nouveau': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }