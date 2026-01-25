Write-Host "Creation des donnees..." -ForegroundColor Green
docker-compose exec backend python manage.py create_test_data
Write-Host "Termine!" -ForegroundColor Green
