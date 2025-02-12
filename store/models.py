from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Liste des choix de catégories
CATEGORIE_CHOICES = [
    ('homme', 'Homme'),
    ('femme', 'Femme'),
    ('enfant', 'Enfant'),
]

# Liste des choix de couleurs
COULEUR_CHOICES = [
    ('rouge', 'Rouge'),
    ('bleu', 'Bleu'),
    ('vert', 'Vert'),
    ('noir', 'Noir'),
    ('blanc', 'Blanc'),
    ('jaune', 'Jaune'),
]

VETEMENTS_CHOICES = [
    # Vêtements pour homme
    ('tshirt_homme', 'T-shirt Homme'),
    ('chemise_homme', 'Chemise Homme'),
    ('polo_homme', 'Polo Homme'),
    ('pull_homme', 'Pull Homme'),
    ('veste_homme', 'Veste Homme'),
    ('manteau_homme', 'Manteau Homme'),
    ('pantalon_homme', 'Pantalon Homme'),
    ('short_homme', 'Short Homme'),
    ('costume_homme', 'Costume Homme'),
    ('sweat_homme', 'Sweatshirt Homme'),
    ('hoodie_homme', 'Hoodie Homme'),
    ('debardeur_homme', 'Débardeur Homme'),
    ('pyjama_homme', 'Pyjama Homme'),
    ('sousvetement_homme', 'Sous-vêtements Homme'),

    # Vêtements pour femme
    ('robe_femme', 'Robe Femme'),
    ('jupe_femme', 'Jupe Femme'),
    ('top_femme', 'Top Femme'),
    ('chemise_femme', 'Chemise Femme'),
    ('veste_femme', 'Veste Femme'),
    ('manteau_femme', 'Manteau Femme'),
    ('pantalon_femme', 'Pantalon Femme'),
    ('short_femme', 'Short Femme'),
    ('combinaison_femme', 'Combinaison Femme'),
    ('pull_femme', 'Pull Femme'),
    ('cardigan_femme', 'Cardigan Femme'),
    ('sweat_femme', 'Sweatshirt Femme'),
    ('hoodie_femme', 'Hoodie Femme'),
    ('sousvetement_femme', 'Sous-vêtements Femme'),
    ('pyjama_femme', 'Pyjama Femme'),

    # Vêtements pour enfant
    ('tshirt_enfant', 'T-shirt Enfant'),
    ('sweat_enfant', 'Sweatshirt Enfant'),
    ('pantalon_enfant', 'Pantalon Enfant'),
    ('short_enfant', 'Short Enfant'),
    ('robe_enfant', 'Robe Enfant'),
    ('jupe_enfant', 'Jupe Enfant'),
    ('veste_enfant', 'Veste Enfant'),
    ('manteau_enfant', 'Manteau Enfant'),
    ('pyjama_enfant', 'Pyjama Enfant'),
    ('body_enfant', 'Body Enfant'),
    ('pull_enfant', 'Pull Enfant'),
    ('sousvetement_enfant', 'Sous-vêtements Enfant'),

    # Vêtements communs
    ('tshirt', 'T-shirt'),
    ('jeans', 'Jeans'),
    ('sweat', 'Sweatshirt'),
    ('pantalon_sport', 'Pantalon de sport'),
    ('baskets', 'Baskets'),
    ('doudoune', 'Doudoune'),
    ('pyjama', 'Pyjama'),
    ('casquette', 'Casquette'),
    ('bonnet', 'Bonnet'),
    ('echarpe', 'Écharpe'),
    ('gants', 'Gants'),
]

class Produit(models.Model):
    nom = models.CharField(
        max_length=100,
        choices=VETEMENTS_CHOICES,
        default='jeans'
    )
    description = models.TextField()
    
    # Champ catégorie avec un menu déroulant
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIE_CHOICES,
        default='homme'
    )
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_en_stock = models.IntegerField()
    image = models.ImageField(upload_to='produits/')
    
    # Champ couleur avec un menu déroulant
    couleur = models.CharField(
        max_length=20,
        choices=COULEUR_CHOICES,
        default='noir'
    )

    date_ajout = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nom



class Panier(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    session_id = models.CharField(max_length=255)  # Gérer le panier par session

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"



class Commentaire(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, related_name='commentaires')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField()
    date_postee = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commentaire de {self.utilisateur} sur {self.produit}'



