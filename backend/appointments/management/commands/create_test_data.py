from django.core.management.base import BaseCommand
from appointments.models import User, Specialite, Cabinet, Professionnel, MotifConsultation, RendezVous
from datetime import date, time
from decimal import Decimal


class Command(BaseCommand):
    help = 'Crée des données de test pour l\'application'

    def handle(self, *args, **options):
        self.stdout.write('Création des données de test...\n')

        # Créer un utilisateur de test
        self.stdout.write('Création de l\'utilisateur de test...')
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
            self.stdout.write(self.style.SUCCESS(f'✓ Utilisateur créé: {user.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'✓ Utilisateur existant: {user.username}'))

        # Créer des spécialités
        self.stdout.write('\nCréation des spécialités...')
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
                self.stdout.write(self.style.SUCCESS(f'✓ Spécialité créée: {nom}'))

        # Créer des cabinets
        self.stdout.write('\nCréation des cabinets...')
        cabinets_data = [
            # Cabinets à Bordeaux (22)
            {'nom': 'Cabinet Médical Victoire', 'adresse': '12 place de la Victoire', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 12 34 56'},
            {'nom': 'Cabinet Saint-Michel', 'adresse': '5 rue Saint-Michel', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 23 45 67'},
            {'nom': 'Cabinet Gambetta', 'adresse': '18 cours Gambetta', 'ville': 'Bordeaux', 'code_postal': '33100', 'telephone': '05 56 34 56 78'},
            {'nom': 'Cabinet Chartrons', 'adresse': '22 rue Notre-Dame', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 45 67 89'},
            {'nom': 'Cabinet Bastide', 'adresse': '8 quai de Queyries', 'ville': 'Bordeaux', 'code_postal': '33100', 'telephone': '05 56 56 78 90'},
            {'nom': 'Cabinet Mériadeck', 'adresse': '15 rue Claude Bonnier', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 67 89 01'},
            {'nom': 'Cabinet Caudéran', 'adresse': '28 avenue du Maréchal Leclerc', 'ville': 'Bordeaux', 'code_postal': '33200', 'telephone': '05 56 78 90 12'},
            {'nom': 'Cabinet Bordeaux Lac', 'adresse': '45 avenue Jean-Gabriel Domergue', 'ville': 'Bordeaux', 'code_postal': '33300', 'telephone': '05 56 89 01 23'},
            {'nom': 'Centre Médical Nansouty', 'adresse': '12 cours de l\'Yser', 'ville': 'Bordeaux', 'code_postal': '33800', 'telephone': '05 56 90 12 34'},
            {'nom': 'Cabinet Saint-Augustin', 'adresse': '34 rue de Tauzia', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 01 23 45'},
            {'nom': 'Cabinet Sainte-Croix', 'adresse': '7 rue Sainte-Croix', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 12 34 67'},
            {'nom': 'Cabinet Jardin Public', 'adresse': '19 cours de Verdun', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 23 45 78'},
            {'nom': 'Cabinet Grand Parc', 'adresse': '25 rue Ferbos', 'ville': 'Bordeaux', 'code_postal': '33300', 'telephone': '05 56 34 56 89'},
            {'nom': 'Cabinet Bacalan', 'adresse': '16 rue Achard', 'ville': 'Bordeaux', 'code_postal': '33300', 'telephone': '05 56 45 67 90'},
            {'nom': 'Cabinet Capucins', 'adresse': '11 place des Capucins', 'ville': 'Bordeaux', 'code_postal': '33800', 'telephone': '05 56 56 78 01'},
            {'nom': 'Cabinet Barrière Saint-Genès', 'adresse': '29 cours de l\'Argonne', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 67 89 12'},
            {'nom': 'Cabinet Quinconces', 'adresse': '3 place des Quinconces', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 78 90 23'},
            {'nom': 'Cabinet Pey-Berland', 'adresse': '14 place Pey-Berland', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 89 01 34'},
            {'nom': 'Cabinet Bourse', 'adresse': '6 place de la Bourse', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 90 12 45'},
            {'nom': 'Cabinet Tourny', 'adresse': '21 allées de Tourny', 'ville': 'Bordeaux', 'code_postal': '33000', 'telephone': '05 56 01 23 56'},
            {'nom': 'Cabinet Barrière du Médoc', 'adresse': '32 cours du Médoc', 'ville': 'Bordeaux', 'code_postal': '33300', 'telephone': '05 56 12 34 78'},
            {'nom': 'Cabinet Croix de Seguey', 'adresse': '40 avenue Émile Counord', 'ville': 'Bordeaux', 'code_postal': '33300', 'telephone': '05 56 23 45 89'},
            
            # Cabinets dans d'autres villes (8)
            {'nom': 'Cabinet Médical République', 'adresse': '15 rue de la République', 'ville': 'Paris', 'code_postal': '75001', 'telephone': '01 23 45 67 89'},
            {'nom': 'Cabinet Vieux-Port', 'adresse': '28 quai du Port', 'ville': 'Marseille', 'code_postal': '13001', 'telephone': '04 91 23 45 67'},
            {'nom': 'Cabinet Bellecour', 'adresse': '10 place Bellecour', 'ville': 'Lyon', 'code_postal': '69002', 'telephone': '04 78 23 45 67'},
            {'nom': 'Cabinet Wilson', 'adresse': '24 place Wilson', 'ville': 'Toulouse', 'code_postal': '31000', 'telephone': '05 61 23 45 67'},
            {'nom': 'Cabinet Massena', 'adresse': '18 place Masséna', 'ville': 'Nice', 'code_postal': '06000', 'telephone': '04 93 23 45 67'},
            {'nom': 'Cabinet Place de Jaude', 'adresse': '12 place de Jaude', 'ville': 'Nantes', 'code_postal': '44000', 'telephone': '02 40 23 45 67'},
            {'nom': 'Cabinet République', 'adresse': '8 place de la République', 'ville': 'Strasbourg', 'code_postal': '67000', 'telephone': '03 88 23 45 67'},
            {'nom': 'Cabinet Grand Place', 'adresse': '16 Grand Place', 'ville': 'Lille', 'code_postal': '59000', 'telephone': '03 20 23 45 67'},
        ]

        for data in cabinets_data:
            cabinet, created = Cabinet.objects.get_or_create(
                nom=data['nom'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Cabinet créé: {data["nom"]}'))

        # Créer des professionnels
        self.stdout.write('\nCréation des professionnels...')
        spec_medecine = Specialite.objects.get(nom='Médecine générale')
        spec_dentiste = Specialite.objects.get(nom='Dentiste')
        spec_cardio = Specialite.objects.get(nom='Cardiologue')
        spec_dermato = Specialite.objects.get(nom='Dermatologue')

        noms = ['Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau',
                'Simon', 'Laurent', 'Lefebvre', 'Michel', 'Garcia', 'David', 'Bertrand', 'Roux', 'Vincent', 'Fournier',
                'Morel', 'Girard', 'Andre', 'Mercier', 'Dupont', 'Lambert', 'Bonnet', 'François', 'Martinez', 'Legrand']
        
        prenoms = ['Sophie', 'Jean', 'Marie', 'Pierre', 'Julie', 'Laurent', 'Isabelle', 'Christophe', 'Nathalie', 'Philippe',
                   'Émilie', 'Marc', 'Catherine', 'Nicolas', 'Sandrine', 'David', 'Valérie', 'Olivier', 'Stéphanie', 'Thomas',
                   'Caroline', 'François', 'Aurélie', 'Sébastien', 'Céline', 'Julien', 'Anne', 'Benoît', 'Martine', 'Patrick']

        specialites = [spec_medecine] * 15 + [spec_dentiste] * 8 + [spec_cardio] * 4 + [spec_dermato] * 3

        professionnels_data = []
        for i in range(30):
            professionnels_data.append({
                'nom': noms[i],
                'prenom': prenoms[i],
                'email': f'{prenoms[i].lower()}.{noms[i].lower()}{i}@medi4ll.fr',
                'specialite': specialites[i],
                'tarif_consultation': Decimal('30.00') if specialites[i] == spec_medecine else Decimal('50.00'),
                'telephone': f'06{i:02d}{i+10:02d}{i+20:02d}{i+30:02d}',
                'numero_rpps': f'{1000000000 + i:011d}',
                'password_hash': 'dummy_hash',
                'statut_validation': 'VALIDE',
                'accepte_teleconsultation': i % 3 == 0,
                'bio': f'Médecin expérimenté en {specialites[i].nom.lower()}, à votre écoute.'
            })

        created_profs = []
        for data in professionnels_data:
            prof, created = Professionnel.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            if created:
                created_profs.append(prof)
                self.stdout.write(self.style.SUCCESS(f'✓ Professionnel créé: Dr. {data["prenom"]} {data["nom"]}'))

        # Lier les professionnels aux cabinets
        self.stdout.write('\nLiaison professionnels-cabinets...')
        
        # Récupérer tous les cabinets
        cabinets_bordeaux = Cabinet.objects.filter(ville='Bordeaux')
        cabinets_autres = Cabinet.objects.exclude(ville='Bordeaux')
        
        # Lier les 22 premiers professionnels aux cabinets de Bordeaux
        for i, prof in enumerate(created_profs[:22]):
            cabinet = cabinets_bordeaux[i % cabinets_bordeaux.count()]
            if not prof.cabinets.filter(id=cabinet.id).exists():
                prof.cabinets.add(cabinet)
                self.stdout.write(self.style.SUCCESS(f'✓ Dr {prof.prenom} {prof.nom} lié au {cabinet.nom}'))
        
        # Lier les 8 derniers professionnels aux cabinets des autres villes
        for i, prof in enumerate(created_profs[22:]):
            cabinet = cabinets_autres[i % cabinets_autres.count()]
            if not prof.cabinets.filter(id=cabinet.id).exists():
                prof.cabinets.add(cabinet)
                self.stdout.write(self.style.SUCCESS(f'✓ Dr {prof.prenom} {prof.nom} lié au {cabinet.nom}'))

        # Créer des motifs de consultation
        self.stdout.write('\nCréation des motifs de consultation...')
        spec_medecine = Specialite.objects.get(nom='Médecine générale')
        spec_dentiste = Specialite.objects.get(nom='Dentiste')
        
        motifs_data = [
            {
                'libelle': 'Consultation générale',
                'duree_estimee': 30,
                'tarif': Decimal('25.00'),
                'specialite': spec_medecine
            },
            {
                'libelle': 'Détartrage',
                'duree_estimee': 45,
                'tarif': Decimal('50.00'),
                'specialite': spec_dentiste
            },
        ]

        for data in motifs_data:
            motif, created = MotifConsultation.objects.get_or_create(
                libelle=data['libelle'],
                specialite=data['specialite'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Motif créé: {data["libelle"]}'))

        # Créer des rendez-vous pour l'utilisateur
        self.stdout.write('\nCréation des rendez-vous...')
        
        # Utiliser les 3 premiers professionnels créés
        if len(created_profs) >= 3:
            prof1 = created_profs[0]
            prof2 = created_profs[1]
            prof3 = created_profs[2]
            
            cabinet1 = prof1.cabinets.first()
            cabinet2 = prof2.cabinets.first()
            cabinet3 = prof3.cabinets.first()
            
            motif_general = MotifConsultation.objects.get(libelle='Consultation générale')

            rendez_vous_data = [
                {
                    'patient': user,
                    'professionnel': prof1,
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
                    'professionnel': prof2,
                    'cabinet': cabinet2,
                    'motif_consultation': motif_general,
                    'date': date(2026, 1, 31),
                    'heure_debut': time(10, 0),
                    'heure_fin': time(10, 45),
                    'statut': 'CONFIRME',
                    'mode': 'PRESENTIEL'
                },
                {
                    'patient': user,
                    'professionnel': prof3,
                    'cabinet': cabinet3,
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
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Rendez-vous créé: {data["date"]} à {data["heure_debut"]} avec Dr. {data["professionnel"].prenom} {data["professionnel"].nom}'
                ))

        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✓ Données de test créées avec succès!'))
        self.stdout.write('='*50)
        self.stdout.write('\nIdentifiants de connexion:')
        self.stdout.write('  Username: maxence')
        self.stdout.write('  Password: password123')
        self.stdout.write('  Email: maxence@test.com\n')
