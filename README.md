# Medi4All 🏥

**Medi4All** est une plateforme de prise de rendez-vous médicaux en ligne, permettant aux patients de trouver et réserver des consultations avec des professionnels de santé.

---

## 📋 Fonctionnalités

### Pour les patients
- 🔍 **Recherche de professionnels** par nom, spécialité, ville
- 📅 **Prise de rendez-vous** en ligne avec calendrier interactif
- 🗺️ **Localisation** des cabinets sur carte interactive (OpenStreetMap)
- 📱 **Gestion des rendez-vous** avec pagination
- 💰 **Filtre par prix** maximum
- 📧 **Contact support** via formulaire

### Pour les professionnels
- 📋 **Gestion des rendez-vous** reçus
- ✅ **Validation/Annulation** des consultations
- 📊 **Tableau de bord** dédié

### Pour les administrateurs
- 👥 **Gestion des utilisateurs** (clients et professionnels)
- 📅 **Gestion des rendez-vous**
- 🛡️ **Accès sécurisé** avec guard de route

---

## 🚀 Installation et lancement

### Prérequis
- Docker et Docker Compose
- Git

### Étapes

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd Medi4ll
```

2. **Lancer les conteneurs Docker**
```bash
docker-compose up -d --build
```

3. **Créer les données de test** (optionnel)
```bash
docker-compose exec backend python manage.py create_test_data
```

4. **Accéder à l'application**
- Frontend : [http://localhost](http://localhost)
- Backend API : [http://localhost:8000](http://localhost:8000)

---

## 🔑 Comptes par défaut

### Administrateur
- **Username** : `admin`
- **Password** : `admin`

### Compte test
- Créés automatiquement avec `create_test_data`
- 32 professionnels de santé
- 4 spécialités disponibles

---

## 🏗️ Architecture

### Stack technique
- **Frontend** : Angular 20 (standalone components)
- **Backend** : Django 4.2.7 + Django REST Framework
- **Base de données** : PostgreSQL 15
- **Serveur web** : Nginx
- **Carte interactive** : Leaflet + OpenStreetMap

### Conteneurs Docker
- `medi4ll-frontend` : Application Angular (port 80)
- `medi4ll-backend` : API Django (port 8000)
- `medi4ll-db` : Base de données PostgreSQL (port 5432)

---

## 📁 Structure du projet

```
Medi4ll/
├── backend/                 # API Django
│   ├── appointments/        # Application principale
│   │   ├── models.py       # Modèles (User, Professionnel, etc.)
│   │   ├── views.py        # Endpoints API
│   │   ├── serializers.py  # Sérialiseurs REST
│   │   └── urls.py         # Routes API
│   └── backend/            # Configuration Django
│
├── src/                    # Application Angular
│   ├── app/
│   │   ├── admin-page/     # Interface admin
│   │   ├── home/           # Page d'accueil
│   │   ├── prise-rdv-page/ # Recherche professionnels
│   │   ├── detail-professionnel/ # Détail + carte
│   │   ├── reservation/    # Liste rendez-vous
│   │   ├── profil-page/    # Profil utilisateur
│   │   └── services/       # Services (Auth, API)
│   └── index.html          # Point d'entrée
│
├── docker-compose.yml      # Configuration Docker
├── Dockerfile             # Image frontend
└── README.md              # Ce fichier
```

---

## 🛠️ Commandes utiles

### Backend Django
```bash
# Créer une migration
docker-compose exec backend python manage.py makemigrations

# Appliquer les migrations
docker-compose exec backend python manage.py migrate

# Créer un superuser
docker-compose exec backend python manage.py createsuperuser

# Voir les logs
docker logs medi4ll-backend --tail 50
```

### Frontend Angular
```bash
# Rebuild le frontend
docker-compose up -d --build frontend

# Voir les logs
docker logs medi4ll-frontend --tail 50
```

### Docker
```bash
# Arrêter les conteneurs
docker-compose down

# Redémarrer un service
docker-compose restart frontend

# Voir l'état des conteneurs
docker-compose ps
```

---

## 🔐 Sécurité

- Authentification par sessions Django
- Route guard pour l'interface admin
- CORS configuré pour localhost
- Mots de passe hashés avec Django

---

## 📝 Endpoints API principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/register/` | POST | Inscription |
| `/api/login/` | POST | Connexion |
| `/api/logout/` | POST | Déconnexion |
| `/api/professionnels/` | GET | Liste professionnels |
| `/api/rendez-vous/` | GET/POST | Rendez-vous patient |
| `/api/admin/rendez-vous/` | GET/DELETE | Admin RDV |
| `/api/admin/clients/` | GET/DELETE | Admin clients |

---

## 👥 Contributeurs

Projet développé dans le cadre du cursus Epitech.

---

## 📄 Licence

Ce projet est à usage éducatif.

