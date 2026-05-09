from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder']  = 'Mot de passe actuel'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nouveau mot de passe'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirmer le nouveau mot de passe'