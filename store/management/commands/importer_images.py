import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Produit

class Command(BaseCommand):
    help = 'Importer toutes les images dans la base avec valeurs aléatoires'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dossier',
            type=str,
            required=True,
            help='Chemin du dossier contenant les images'
        )

    def handle(self, *args, **options):
        base_dir = options['dossier']
        categories = ['homme', 'femme', 'enfant']

        fichiers = [f for f in os.listdir(base_dir) if f.lower().endswith(".jpg")]
        total = len(fichiers)
        self.stdout.write(self.style.SUCCESS(f"⚡ {total} images trouvées dans {base_dir}"))

        for i, filename in enumerate(fichiers, 1):
            path = os.path.join(base_dir, filename)
            categorie = random.choice(categories)
            prix = round(random.uniform(1000, 5000), 2)
            couleur = random.choice(['rouge', 'bleu', 'noir', 'blanc', 'rose', 'vert', 'jaune', 'gris'])
            
            try:
                with open(path, "rb") as f:
                    produit = Produit(
                        nom=f"Vêtement {categorie}",
                        description=f"Vêtement importé ({filename})",
                        categorie=categorie,
                        prix=prix,
                        quantite_en_stock=500,
                        couleur=couleur,
                        populaire=random.choice([True, False]),
                        nouveau=random.choice([True, False]),
                    )
                    produit.image.save(filename, File(f))
                    produit.save()
                self.stdout.write(self.style.SUCCESS(f"[{i}/{total}] ✅ {filename} -> {categorie} | {couleur} | {prix}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[{i}/{total}] ❌ {filename} erreur: {e}"))
