python manage.py shell << EOF
from appointments.models import User
try:
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.is_admin = True
    u.save()
    print(f"Admin créé/mis à jour:")
    print(f"  Username: admin")
    print(f"  Email: {u.email}")
    print(f"  Password: admin123")
except User.DoesNotExist:
    print("Admin non trouvé")
EOF
