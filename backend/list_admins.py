from appointments.models import User

print("=== Liste des utilisateurs admin ===\n")
admins = User.objects.filter(is_admin=True)

if admins.count() == 0:
    print("Aucun admin trouvé dans la base de données.")
else:
    for u in admins:
        print(f"Username: {u.username}")
        print(f"Email: {u.email}")
        print(f"Nom: {u.first_name} {u.last_name}")
        print("-" * 40)

print(f"\nTotal: {admins.count()} admin(s)")

print("\n=== Liste de tous les utilisateurs ===\n")
all_users = User.objects.all()
for u in all_users:
    print(f"Username: {u.username} | Email: {u.email} | Admin: {u.is_admin}")
