# Script PowerShell pour créer les données de test
Write-Host "Création des données de test..." -ForegroundColor Green
docker-compose exec backend python manage.py create_test_data

Write-Host "`n✓ Terminé! Vous pouvez maintenant vous connecter avec:" -ForegroundColor Green
Write-Host "  Username: maxence" -ForegroundColor Yellow
Write-Host "  Password: password123" -ForegroundColor Yellow
