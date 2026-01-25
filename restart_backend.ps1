# Script pour redémarrer le backend Docker
Write-Host "Redémarrage du backend..." -ForegroundColor Cyan
docker-compose restart backend

Write-Host "`n✓ Backend redémarré!" -ForegroundColor Green
Write-Host "`nAttendez 5 secondes que le serveur démarre..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host "`n✓ Vous pouvez maintenant vous reconnecter!" -ForegroundColor Green
Write-Host "Username: maxence" -ForegroundColor Yellow
Write-Host "Password: password123" -ForegroundColor Yellow
