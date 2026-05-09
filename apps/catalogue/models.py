import re
from django.db import models


# ---------------------------------------------------------------------------
# Choices — kept as module-level tuples (Django convention)
# ---------------------------------------------------------------------------

class Categorie(models.TextChoices):
    HOMME = 'homme', 'Homme'
    FEMME = 'femme', 'Femme'
    ENFANT = 'enfant', 'Enfant'


class Couleur(models.TextChoices):
    ROUGE = 'rouge', 'Rouge'
    BLEU = 'bleu', 'Bleu'
    VERT = 'vert', 'Vert'
    NOIR = 'noir', 'Noir'
    BLANC = 'blanc', 'Blanc'
    JAUNE = 'jaune', 'Jaune'
    GRIS = 'gris', 'Gris'
    MARRON = 'marron', 'Marron'
    ROSE = 'rose', 'Rose'
    ORANGE = 'orange', 'Orange'


VETEMENTS_CHOICES = [
    # ── Homme ──
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
    # ── Femme ──
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
    # ── Enfant ──
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
    # ── Communs ──
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

_GDRIVE_ID_RE = re.compile(r'id=([a-zA-Z0-9_-]+)')


class ProduitManager(models.Manager):
    """Custom manager with common querysets."""

    def populaires(self):
        return self.filter(populaire=True).order_by('-date_ajout')

    def nouveaux(self):
        return self.filter(nouveau=True).order_by('-date_ajout')

    def par_categorie(self, categorie: str):
        return self.filter(categorie=categorie).order_by('-date_ajout')

    def en_stock(self):
        return self.filter(quantite_en_stock__gt=0)


class Produit(models.Model):
    """
    Represents a clothing product.

    The `nom` field uses choices to standardise product type names.
    `image_url` supports Google Drive shared links, which are normalised
    by `get_image()` — business logic confined to this single method.
    """

    nom = models.CharField(
        max_length=100,
        choices=VETEMENTS_CHOICES,
        default='jeans',
        verbose_name='Type de vêtement',
    )
    description = models.TextField(verbose_name='Description')
    categorie = models.CharField(
        max_length=20,
        choices=Categorie.choices,
        default=Categorie.HOMME,
        verbose_name='Catégorie',
        db_index=True,
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Prix (HTG)',
    )
    quantite_en_stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Quantité en stock',
    )
    image_url = models.URLField(blank=True, null=True, verbose_name='URL image externe')
    image = models.ImageField(
        upload_to='produits/',
        blank=True,
        null=True,
        verbose_name='Image locale',
    )
    couleur = models.CharField(
        max_length=20,
        choices=Couleur.choices,
        default=Couleur.NOIR,
        verbose_name='Couleur',
    )
    populaire = models.BooleanField(default=False, verbose_name='Populaire', db_index=True)
    nouveau = models.BooleanField(default=False, verbose_name='Nouveau', db_index=True)
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'ajout')

    objects = ProduitManager()

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['-date_ajout']

    def __str__(self) -> str:
        return self.get_nom_display()

    @property
    def is_en_stock(self) -> bool:
        return self.quantite_en_stock > 0

    def get_image(self) -> str | None:
        """Return the best available image URL for this product.

        Normalises Google Drive sharing URLs to a direct-access format
        compatible with <img> tags (no authentication required).
        """
        if self.image_url:
            if 'drive.google.com' in self.image_url or 'drive.usercontent.google.com' in self.image_url:
                match = _GDRIVE_ID_RE.search(self.image_url)
                if match:
                    return f'https://lh3.googleusercontent.com/d/{match.group(1)}'
            return self.image_url
        if self.image:
            return self.image.url
        return None
