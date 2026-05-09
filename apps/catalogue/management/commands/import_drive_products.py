"""
Management command: import_drive_products
-----------------------------------------
Imports product images from a Google Drive folder and creates Produit records.

Usage:
    python manage.py import_drive_products
    python manage.py import_drive_products --folder-id FOLDER_ID
    python manage.py import_drive_products --dry-run

Dependencies (add to requirements.txt if not present):
    google-api-python-client
    google-auth
"""
import random
from time import sleep

from django.core.management.base import BaseCommand, CommandError

from apps.catalogue.models import Produit, VETEMENTS_CHOICES, Categorie, Couleur

# Colour keywords → choice value (FR + EN)
COLOUR_KEYWORDS = {
    'rouge': 'rouge', 'red': 'rouge',
    'bleu': 'bleu',   'blue': 'bleu',
    'vert': 'vert',   'green': 'vert',
    'noir': 'noir',   'black': 'noir',
    'blanc': 'blanc', 'white': 'blanc',
    'jaune': 'jaune', 'yellow': 'jaune',
    'gris': 'gris',   'gray': 'gris', 'grey': 'gris',
    'marron': 'marron', 'brown': 'marron',
    'rose': 'rose',   'pink': 'rose',
    'orange': 'orange',
}

# Clothing keywords → suffix (combined with category later)
GARMENT_KEYWORDS = {
    'tshirt': 'tshirt', 't-shirt': 'tshirt',
    'chemise': 'chemise', 'shirt': 'chemise',
    'polo': 'polo',
    'pull': 'pull', 'sweater': 'pull',
    'veste': 'veste', 'jacket': 'veste',
    'manteau': 'manteau', 'coat': 'manteau',
    'pantalon': 'pantalon', 'trousers': 'pantalon', 'pants': 'pantalon',
    'short': 'short', 'shorts': 'short',
    'costume': 'costume', 'suit': 'costume',
    'sweat': 'sweat', 'sweatshirt': 'sweat',
    'hoodie': 'hoodie',
    'debardeur': 'debardeur', 'tank': 'debardeur',
    'pyjama': 'pyjama', 'pajama': 'pyjama',
    'robe': 'robe', 'dress': 'robe',
    'jupe': 'jupe', 'skirt': 'jupe',
    'top': 'top',
    'combinaison': 'combinaison', 'jumpsuit': 'combinaison',
    'cardigan': 'cardigan',
    'body': 'body',
    'jean': 'jeans', 'jeans': 'jeans',
    'basket': 'baskets', 'sneaker': 'baskets',
    'doudoune': 'doudoune', 'puffer': 'doudoune',
    'casquette': 'casquette', 'cap': 'casquette',
    'bonnet': 'bonnet', 'beanie': 'bonnet',
    'echarpe': 'echarpe', 'scarf': 'echarpe',
    'gant': 'gants', 'glove': 'gants',
}

_VALID_VETEMENTS = {v[0] for v in VETEMENTS_CHOICES}
_VALID_COULEURS  = {c[0] for c in Couleur.choices}
_VALID_CATS      = {c[0] for c in Categorie.choices}


class Command(BaseCommand):
    help = "Import products from a Google Drive folder (images linked by URL, not downloaded)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--folder-id',
            default='1uC-1nUvD4iaUDhdL1d-h06yshZJTCvm2',
            help='Google Drive folder ID to import from.',
        )
        parser.add_argument(
            '--credentials',
            default='/home/baoulyStore/credentials/baoulystoredrive-5910b996c8ce.json',
            help='Path to the Google service account JSON credentials file.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate import without writing to the database.',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Log progress every N products.',
        )

    def handle(self, *args, **options):
        try:
            from googleapiclient.discovery import build
            from google.oauth2 import service_account
        except ImportError:
            raise CommandError(
                "google-api-python-client is required.\n"
                "Install it with: pip install google-api-python-client google-auth"
            )

        folder_id   = options['folder_id']
        creds_path  = options['credentials']
        dry_run     = options['dry_run']
        batch_size  = options['batch_size']

        self.stdout.write(self.style.NOTICE(
            f"{'[DRY RUN] ' if dry_run else ''}Starting import from folder: {folder_id}"
        ))

        try:
            creds = service_account.Credentials.from_service_account_file(
                creds_path,
                scopes=['https://www.googleapis.com/auth/drive.readonly'],
            )
            svc = build('drive', 'v3', credentials=creds)
        except FileNotFoundError:
            raise CommandError(f"Credentials file not found: {creds_path}")

        page_token  = None
        total       = 0
        errors      = 0

        while True:
            results = svc.files().list(
                q=f"'{folder_id}' in parents and mimeType contains 'image/'",
                fields="nextPageToken, files(id, name, mimeType)",
                pageSize=1000,
                pageToken=page_token,
            ).execute()

            for file in results.get('files', []):
                try:
                    file_id  = file['id']
                    filename = file['name']
                    image_url = f"https://drive.google.com/uc?export=view&id={file_id}"

                    categorie = self._detect_categorie(filename)
                    nom       = self._detect_garment(filename, categorie)
                    couleur   = self._detect_couleur(filename)

                    if not dry_run:
                        Produit.objects.create(
                            nom=nom,
                            description=f"Importé depuis Google Drive — {filename}",
                            categorie=categorie,
                            prix=random.randint(1000, 1500),
                            quantite_en_stock=random.randint(50, 500),
                            couleur=couleur,
                            populaire=random.choice([True, False]),
                            nouveau=random.choice([True, True, False]),
                            image_url=image_url,
                        )

                    total += 1
                    if total % batch_size == 0:
                        self.stdout.write(self.style.SUCCESS(f"  ✔ {total} products processed…"))
                        if not dry_run:
                            sleep(0.5)   # light throttle; reduce if needed

                except Exception as exc:
                    errors += 1
                    self.stdout.write(self.style.ERROR(f"  ✗ Error on '{file.get('name')}': {exc}"))

            page_token = results.get('nextPageToken')
            if not page_token:
                break

        action = "would be created" if dry_run else "created"
        self.stdout.write(self.style.SUCCESS(
            f"\nImport complete: {total} products {action}, {errors} errors."
        ))

    # ── Helpers ────────────────────────────────────────────────────────────

    def _detect_categorie(self, filename: str) -> str:
        nl = filename.lower()
        if any(w in nl for w in ('homme', 'men', 'man')):
            return 'homme'
        if any(w in nl for w in ('femme', 'women', 'woman')):
            return 'femme'
        if any(w in nl for w in ('enfant', 'kid', 'child', 'bebe', 'baby')):
            return 'enfant'
        return random.choice(list(_VALID_CATS))

    def _detect_garment(self, filename: str, categorie: str) -> str:
        nl = filename.lower()
        for keyword, base in GARMENT_KEYWORDS.items():
            if keyword in nl:
                candidate = f"{base}_{categorie}"
                if candidate in _VALID_VETEMENTS:
                    return candidate
                if base in _VALID_VETEMENTS:
                    return base
        # Fallback: first valid garment for this category
        fallbacks = {
            'homme': 'tshirt_homme',
            'femme': 'robe_femme',
            'enfant': 'tshirt_enfant',
        }
        return fallbacks.get(categorie, 'jeans')

    def _detect_couleur(self, filename: str) -> str:
        nl = filename.lower()
        for keyword, couleur in COLOUR_KEYWORDS.items():
            if keyword in nl and couleur in _VALID_COULEURS:
                return couleur
        return random.choice(list(_VALID_COULEURS))
