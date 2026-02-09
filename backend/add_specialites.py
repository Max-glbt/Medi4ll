import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from appointments.models import Specialite

specialites = [
    ('Médecine générale', 'Consultation générale et suivi médical'),
    ('Dentiste', 'Soins dentaires et orthodontie'),
    ('Ophtalmologue', 'Spécialiste des yeux et de la vision'),
    ('Kinésithérapeute', 'Rééducation et réadaptation fonctionnelle'),
]

for nom, desc in specialites:
    spec, created = Specialite.objects.get_or_create(
        nom=nom,
        defaults={'description': desc}
    )
    if created:
        print(f"Spécialité créée: {nom}")
    else:
        print(f"Spécialité existante: {nom}")

