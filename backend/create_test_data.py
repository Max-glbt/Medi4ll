"""
Script pour créer des données de test dans la base de données
Exécutez avec: docker-compose exec backend python create_test_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from appointments.models import User, Specialite, Cabinet, Professionnel, MotifConsultation, RendezVous
from datetime import date, time
from decimal import Decimal

# Créer un utilisateur de test
print("Création de l'utilisateur de test...")
user, created = User.objects.get_or_create(
    username='maxence',
    defaults={
        'email': 'maxence@test.com',
        'first_name': 'Maxence',
        'last_name': 'Test',
        'telephone': '0612345678',
        'date_naissance': date(1995, 5, 15),
        'sexe': 'M'
    }
)
if created:
    user.set_password('password123')
    user.save()
    print(f"✓ Utilisateur créé: {user.username}")
else:
    print(f"✓ Utilisateur existant: {user.username}")

# Créer des spécialités
print("\nCréation des spécialités...")
specialites = [
    ('Médecine générale', 'Consultation générale et suivi médical'),
    ('Dentiste', 'Soins dentaires et orthodontie'),
    ('Cardiologue', 'Spécialiste du cœur et système cardiovasculaire'),
    ('Dermatologue', 'Spécialiste de la peau'),
]

for nom, desc in specialites:
    spec, created = Specialite.objects.get_or_create(
        nom=nom,
        defaults={'description': desc}
    )
    if created:
        print(f"✓ Spécialité créée: {nom}")

# Créer des cabinets
print("\nCréation des cabinets...")
cabinets_data = [
    {
        'nom': 'Cabinet Médical Centre-Ville',
        'adresse': '15 rue de la République',
        'ville': 'Paris',
        'code_postal': '75001',
        'telephone': '01 23 45 67 89'
    },
    {
        'nom': 'Cabinet Dentaire Saint-Michel',
        'adresse': '8 avenue des Champs',
        'ville': 'Paris',
        'code_postal': '75008',
        'telephone': '01 98 76 54 32'
    }
]

for data in cabinets_data:
    cabinet, created = Cabinet.objects.get_or_create(
        nom=data['nom'],
        defaults=data
    )
    if created:
        print(f"✓ Cabinet créé: {data['nom']}")

# Créer des professionnels
print("\nCréation des professionnels...")
spec_medecine = Specialite.objects.get(nom='Médecine générale')
spec_dentiste = Specialite.objects.get(nom='Dentiste')
cabinet1 = Cabinet.objects.get(nom='Cabinet Médical Centre-Ville')
cabinet2 = Cabinet.objects.get(nom='Cabinet Dentaire Saint-Michel')

professionnels_data = [
    {
        'nom': 'Martin',
        'prenom': 'Sophie',
        'email': 'sophie.martin@email.com',
        'specialite': spec_medecine,
        'cabinet': cabinet1,
        'tarif_consultation': Decimal('25.00')
    },
    {
        'nom': 'Dupont',
        'prenom': 'Jean',
        'email': 'jean.dupont@email.com',
        'specialite': spec_dentiste,
        'cabinet': cabinet2,
        'tarif_consultation': Decimal('50.00')
    }
]

for data in professionnels_data:
    prof, created = Professionnel.objects.get_or_create(
        email=data['email'],
        defaults=data
    )
    if created:
        print(f"✓ Professionnel créé: Dr. {data['prenom']} {data['nom']}")

# Créer des motifs de consultation
print("\nCréation des motifs de consultation...")
motifs_data = [
    {'libelle': 'Consultation générale', 'duree_estimee': 30, 'tarif': Decimal('25.00')},
    {'libelle': 'Détartrage', 'duree_estimee': 45, 'tarif': Decimal('50.00')},
]

for data in motifs_data:
    motif, created = MotifConsultation.objects.get_or_create(
        libelle=data['libelle'],
        defaults=data
    )
    if created:
        print(f"✓ Motif créé: {data['libelle']}")

# Créer des rendez-vous pour l'utilisateur
print("\nCréation des rendez-vous...")
prof_martin = Professionnel.objects.get(email='sophie.martin@email.com')
prof_dupont = Professionnel.objects.get(email='jean.dupont@email.com')
motif_general = MotifConsultation.objects.get(libelle='Consultation générale')
motif_dentaire = MotifConsultation.objects.get(libelle='Détartrage')

rendez_vous_data = [
    {
        'patient': user,
        'professionnel': prof_martin,
        'cabinet': cabinet1,
        'motif_consultation': motif_general,
        'date': date(2026, 1, 27),
        'heure_debut': time(14, 30),
        'heure_fin': time(15, 0),
        'statut': 'CONFIRME',
        'mode': 'PRESENTIEL'
    },
    {
        'patient': user,
        'professionnel': prof_dupont,
        'cabinet': cabinet2,
        'motif_consultation': motif_dentaire,
        'date': date(2026, 1, 31),
        'heure_debut': time(10, 0),
        'heure_fin': time(10, 45),
        'statut': 'CONFIRME',
        'mode': 'PRESENTIEL'
    },
    {
        'patient': user,
        'professionnel': prof_martin,
        'cabinet': cabinet1,
        'motif_consultation': motif_general,
        'date': date(2026, 2, 5),
        'heure_debut': time(9, 0),
        'heure_fin': time(9, 30),
        'statut': 'EN_ATTENTE',
        'mode': 'TELECONSULTATION'
    }
]

for data in rendez_vous_data:
    rdv, created = RendezVous.objects.get_or_create(
        patient=data['patient'],
        professionnel=data['professionnel'],
        date=data['date'],
        heure_debut=data['heure_debut'],
        defaults=data
    )
    if created:
        print(f"✓ Rendez-vous créé: {data['date']} à {data['heure_debut']} avec Dr. {data['professionnel'].prenom} {data['professionnel'].nom}")

print("\n" + "="*50)
print("✓ Données de test créées avec succès!")
print("="*50)
print(f"\nIdentifiants de connexion:")
print(f"  Username: maxence")
print(f"  Password: password123")
print(f"  Email: maxence@test.com")
