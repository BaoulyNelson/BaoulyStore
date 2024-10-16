from django import forms
from django.contrib.auth.models import User
from .models import Commentaire

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Nom")
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Message")

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


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['texte']
