# Plan d'implémentation — Location & Vente Immobilier

## Les 3 Acteurs

| Acteur | Rôle | Accès |
|--------|------|-------|
| **Admin** | Supervise tout le système | Gestion des utilisateurs, biens, catégories, statistiques globales |
| **Propriétaire/Agence** | Gère son patrimoine | Ses biens, ses locataires, ses baux, sa comptabilité |
| **Locataire** | Consulte son espace | Son bail, ses paiements, ses quittances |

---

## Architecture

```
location/
├── backend/
│   ├── config/                   # Settings, URLs
│   ├── users/                    # Auth + rôles (admin, owner, tenant)
│   ├── properties/               # Biens, Catégories, Types
│   ├── tenants/                  # Locataires, Baux
│   ├── accounting/               # Paiements, Dépenses, Balance
│   ├── notifications/            # Alertes, Documents PDF
│   └── .env                      # Variables Neon, Secret Key
├── frontend/
│   ├── app/
│   │   ├── (auth)/               # Login, Register (commun)
│   │   ├── (admin)/              # ← Interface ADMIN
│   │   │   ├── dashboard/
│   │   │   ├── users/
│   │   │   ├── properties/
│   │   │   └── settings/
│   │   ├── (owner)/              # ← Interface PROPRIÉTAIRE/AGENCE
│   │   │   ├── dashboard/
│   │   │   ├── properties/
│   │   │   ├── tenants/
│   │   │   └── accounting/
│   │   ├── (tenant)/             # ← Interface LOCATAIRE
│   │   │   ├── dashboard/
│   │   │   ├── lease/
│   │   │   └── payments/
│   │   ├── components/
│   │   └── lib/                  # API client, helpers
```

---

## Proposed Changes

### Backend

#### [MODIFY] [settings.py](file:///home/pekpeli-gnimdou-kevin/Documents/projets/location/backend/config/settings.py)

- Ajouter `rest_framework`, `corsheaders` dans INSTALLED_APPS
- Configurer Neon PostgreSQL via `dj-database-url` + `.env`
- Configurer CORS, REST Framework, et AUTH_USER_MODEL custom

#### [NEW] [.env](file:///home/pekpeli-gnimdou-kevin/Documents/projets/location/backend/.env)

```env
DATABASE_URL=postgresql://...@ep-xxx.neon.tech/neondb?sslmode=require
SECRET_KEY=xxx
DEBUG=True
```

#### Nouvelles dépendances Python

```bash
pip install dj-database-url python-decouple psycopg2-binary
```

---

### App `users` — Modèle User Custom

```python
class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrateur'),
        ('owner', 'Propriétaire/Agence'),
        ('tenant', 'Locataire'),
    ]
    role = CharField(max_length=10, choices=ROLES)
    phone = CharField(max_length=20, blank=True)
    avatar = ImageField(upload_to='avatars/', blank=True)
```

### App `properties` — Patrimoine

```python
class Category       # Appartement, Maison, Bureau, Terrain...
class PropertyType   # Studio, Chambre salon, Suite... (lié à Category)
class Property       # Adresse, photos, loyer, statut, géoloc, owner (FK User)
class Equipment      # Climatisation, Piscine... (M2M avec Property)
```

### App `tenants` — Locataires & Baux

```python
class Tenant   # Nom, email, téléphone, profession, pièce d'identité, garant
class Lease    # Property, Tenant, dates, loyer, dépôt, révision annuelle
```

### App `accounting` — Comptabilité

```python
class Payment  # Lease, montant, date, statut, méthode
class Expense  # Property, type, montant, facture
class AuditLog # Historisation de toutes les modifications
```

---

## Verification Plan

### Tests automatisés
```bash
python3 manage.py check          # Vérifier la config
python3 manage.py migrate        # Créer les tables sur Neon
python3 manage.py createsuperuser  # Créer un admin
python3 manage.py runserver      # Tester l'accès
```

### Vérification manuelle
- Admin Django accessible sur `http://localhost:8000/admin/`
- Tables créées sur le dashboard Neon
- API DRF accessible sur `http://localhost:8000/api/`

---

## User Review Required

> [!IMPORTANT]
> **En attente** : Envoyez-moi la **connection string Neon** pour que je configure le backend.
