# Instructions pour créer les données de test

## Étapes à suivre dans un nouveau terminal PowerShell :

1. **Fermer le shell Django actuellement ouvert** (taper `exit()` ou Ctrl+C)

2. **Créer les données de test**:
```powershell
docker-compose exec backend python manage.py create_test_data
```

3. **Se connecter avec les identifiants de test**:
   - Username: `maxence`
   - Password: `password123`
   - Email: `maxence@test.com`

## Utilisation dans l'application Angular

Une fois les données créées, vous pourrez :
1. Vous connecter avec les identifiants ci-dessus
2. Voir les 3 rendez-vous créés pour l'utilisateur "maxence" sur la page "Mes rendez-vous"

## Tests de l'API

### Test de connexion
```powershell
curl -X POST http://localhost:8000/api/login/ -H "Content-Type: application/json" -d '{\"username\":\"maxence\",\"password\":\"password123\"}'
```

### Test récupération des rendez-vous (après connexion)
```powershell
curl http://localhost:8000/api/rendez-vous/
```
