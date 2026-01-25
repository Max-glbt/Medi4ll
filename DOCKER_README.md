# Medi4ll - Docker Setup

## Architecture

L'application est composée de 3 conteneurs Docker :

1. **database** - PostgreSQL 15 (Base de données)
2. **backend** - Django API (Backend REST API)
3. **frontend** - Angular + Nginx (Interface utilisateur)

## Prérequis

- Docker Desktop installé
- Docker Compose installé

## Démarrage rapide

### 1. Construire et démarrer tous les conteneurs

```bash
docker-compose up --build
```

### 2. Accéder à l'application

- **Frontend** : http://localhost
- **Backend API** : http://localhost:8000
- **Admin Django** : http://localhost:8000/admin

### 3. Arrêter les conteneurs

```bash
docker-compose down
```

### 4. Arrêter et supprimer les volumes (données)

```bash
docker-compose down -v
```

## Commandes utiles

### Voir les logs

```bash
# Tous les conteneurs
docker-compose logs -f

# Un conteneur spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

### Exécuter des commandes dans un conteneur

```bash
# Backend - Créer un superuser
docker-compose exec backend python manage.py createsuperuser

# Backend - Migrations
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# Accéder au shell Django
docker-compose exec backend python manage.py shell

# Accéder au shell PostgreSQL
docker-compose exec database psql -U medi4ll_user -d medi4ll
```

### Reconstruire un conteneur spécifique

```bash
docker-compose up --build backend
docker-compose up --build frontend
```

## Variables d'environnement

Les variables sont configurées dans le `docker-compose.yml`. Pour la production, utilisez un fichier `.env` :

```env
# Backend
DEBUG=0
SECRET_KEY=your-secret-key-here
DATABASE_NAME=medi4ll
DATABASE_USER=medi4ll_user
DATABASE_PASSWORD=medi4ll_password
DATABASE_HOST=database
DATABASE_PORT=5432
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Database
POSTGRES_DB=medi4ll
POSTGRES_USER=medi4ll_user
POSTGRES_PASSWORD=medi4ll_password
```

## Structure des fichiers

```
Medi4ll/
├── docker-compose.yml          # Orchestration des conteneurs
├── Dockerfile                  # Build du frontend Angular
├── nginx.conf                  # Configuration Nginx
├── .dockerignore              # Fichiers à exclure du build frontend
├── backend/
│   ├── Dockerfile             # Build du backend Django
│   ├── requirements.txt       # Dépendances Python
│   └── .dockerignore         # Fichiers à exclure du build backend
└── src/                       # Code source Angular
```

## Développement

### Mode développement avec hot-reload

Pour le développement, vous pouvez monter les volumes :

```bash
# Le backend est déjà configuré avec le volume monté
# Pour le frontend, lancez-le en local :
npm start
```

### Production

Pour la production, modifiez `docker-compose.yml` :

1. Changez `DEBUG=0`
2. Utilisez un `SECRET_KEY` fort
3. Configurez `ALLOWED_HOSTS` et `CORS_ALLOWED_ORIGINS`
4. Utilisez des mots de passe forts pour PostgreSQL
5. Ajoutez SSL/TLS

## Troubleshooting

### Le backend ne démarre pas

Vérifiez que la base de données est prête :
```bash
docker-compose logs database
```

### Erreur de connexion à la base de données

Attendez que le healthcheck de PostgreSQL soit OK :
```bash
docker-compose ps
```

### Rebuild complet

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```
