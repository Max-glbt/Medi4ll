# Script pour créer rapidement l'utilisateur de test via l'API
Write-Host "Création de l'utilisateur de test..." -ForegroundColor Cyan

$body = @{
    username = "maxence"
    email = "maxence@test.com"
    password = "password123"
    first_name = "Maxence"
    last_name = "Test"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/register/" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✓ Utilisateur créé avec succès!" -ForegroundColor Green
    Write-Host "Username: maxence" -ForegroundColor Yellow
    Write-Host "Password: password123" -ForegroundColor Yellow
} catch {
    if ($_.Exception.Response.StatusCode -eq 400) {
        Write-Host "⚠ L'utilisateur existe déjà" -ForegroundColor Yellow
        Write-Host "Vous pouvez vous connecter avec:" -ForegroundColor Cyan
        Write-Host "Username: maxence" -ForegroundColor Yellow
        Write-Host "Password: password123" -ForegroundColor Yellow
    } else {
        Write-Host "✗ Erreur: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nMaintenant exécutez la commande pour créer toutes les données:" -ForegroundColor Cyan
Write-Host "docker-compose exec backend python manage.py create_test_data" -ForegroundColor White
