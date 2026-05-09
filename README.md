# Baouly's Store — Django E-commerce

Application e-commerce de vêtements pour Haïti, avec paiement MonCash intégré.

---

## 🏗️ Architecture

```
BaoulyStore/
├── config/                    # Configuration Django
│   ├── settings/
│   │   ├── base.py            # Settings communs
│   │   ├── development.py     # Dev (email console, no SSL)
│   │   └── production.py      # Prod (SSL, security headers)
│   ├── urls.py                # Routage principal
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── catalogue/             # Produits (listing, détail, CRUD staff)
│   │   ├── models.py          # Produit + ProduitManager
│   │   ├── services.py        # Logique métier catalogue
│   │   ├── views.py           # Vues (thin — délèguent aux services)
│   │   ├── forms.py
│   │   ├── admin.py
│   │   ├── urls.py
│   │   └── management/commands/import_drive_products.py
│   │
│   ├── cart/                  # Panier session + paiement MonCash
│   │   ├── models.py          # CartItem
│   │   ├── services.py        # Logique panier + MonCash (isolé)
│   │   ├── context_processors.py  # cart_count/cart_total (sans appel MonCash)
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── reviews/               # Témoignages clients
│   ├── accounts/              # Authentification (login/signup/profil/reset)
│   └── pages/                 # Pages statiques (contact, FAQ, blog…)
│
├── templates/
│   ├── base.html              # Base principale (dashboard/connecté)
│   ├── auth_base.html         # Base pages auth (sans nav complète)
│   ├── partials/              # header, footer, modal, messages
│   ├── catalogue/
│   ├── cart/
│   ├── reviews/
│   ├── accounts/
│   └── pages/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🚀 Installation

### 1. Cloner et préparer l'environnement

```bash
git clone <repo-url> BaoulyStore
cd BaoulyStore
python -m venv venv
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate             # Windows
pip install -r requirements.txt
```

### 2. Variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec vos vraies valeurs
```

Variables requises dans `.env` :

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Clé secrète Django (générer une nouvelle) |
| `DJANGO_ALLOWED_HOSTS` | Hosts autorisés, séparés par des virgules |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Connexion MySQL |
| `MONCASH_CLIENT_ID`, `MONCASH_SECRET_ID` | Clés API MonCash |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Gmail SMTP |

### 3. Base de données

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Lancer le serveur

```bash
python manage.py runserver
```

---

## 🔧 Commandes utiles

```bash
# Importer des produits depuis Google Drive
python manage.py import_drive_products
python manage.py import_drive_products --folder-id VOTRE_ID --dry-run

# Collecter les fichiers statiques (production)
python manage.py collectstatic --noinput
```

---

## 🔐 Sécurité

- Les clés API et mots de passe sont dans `.env` (jamais commités)
- Protection CSRF activée sur toutes les vues POST
- Authentification requise pour ajouter au panier et gérer le profil
- Vues staff protégées par `@user_passes_test(is_staff)`
- En production : HTTPS obligatoire, HSTS activé

---

## 💳 Paiement MonCash

L'URL de paiement MonCash est générée **uniquement** lors de l'affichage du panier (`/panier/`), pas à chaque chargement de page. Cela évite des appels API externes inutiles sur chaque requête.

Pour tester en sandbox, laisser `MONCASH_DEBUG=True` dans `.env`.

---

## 🧩 Extensions possibles

- **Commandes** : ajouter un modèle `Order` + `OrderItem` pour l'historique
- **Cart persistant** : migrer le panier session vers un panier lié à l'utilisateur
- **Tests** : les `services.py` sont 100% testables sans requête HTTP
- **API REST** : les services sont prêts pour être exposés via DRF
- **Cache** : ajouter `django-redis` pour cacher les listes de produits populaires
