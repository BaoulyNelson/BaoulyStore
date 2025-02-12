from django import forms
from django.contrib.auth.models import User
from .models import Commentaire,Produit


from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre nom"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Votre email"})
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Votre message"})
    )



class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='Email ou Nom d\'utilisateur')
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirmer le mot de passe')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hashage du mot de passe
        if commit:
            user.save()
        return user


# Formulaire pour mettre à jour le profil de l'utilisateur
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
      
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'categorie', 'prix', 'quantite_en_stock', 'image', 'couleur']
        labels = {
            'nom': 'Titre du Produit',
            'description': 'Description',
            'categorie': 'Catégorie',
            'prix': 'Prix',
            'quantite_en_stock': 'Quantité en Stock',
            'image': 'Image du Produit',
            'couleur': 'Couleur'
        }
        widgets = {
            'nom': forms.Select(),  # Menu déroulant pour le choix du nom
            'categorie': forms.Select(),  # Menu déroulant pour la catégorie
            'couleur': forms.Select(),  # Menu déroulant pour la couleur
            'description': forms.Textarea(attrs={'rows': 4}),
            'prix': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'quantite_en_stock': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
        }

           
class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['texte']
