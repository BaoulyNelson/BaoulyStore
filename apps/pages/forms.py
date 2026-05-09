from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Nom", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'}),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Votre message…'}),
    )
