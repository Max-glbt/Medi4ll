from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class User(AbstractUser):
    """Patient"""
    date_naissance = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, null=True, blank=True)
    
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    telephone_urgence = models.CharField(max_length=20, blank=True, verbose_name="Téléphone d'urgence")
    
    adresse_complete = models.TextField(blank=True, verbose_name="Adresse complète")
    ville = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(max_length=10, blank=True)
    pays = models.CharField(max_length=100, default='France')
    
    numero_securite_sociale = models.CharField(max_length=15, blank=True, unique=True, null=True, 
                                                verbose_name="Numéro de sécurité sociale")
    
    derniere_connexion = models.DateTimeField(null=True, blank=True, verbose_name="Dernière connexion")
    
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    
    PREFERENCE_NOTIF_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('les_deux', 'Email et SMS'),
        ('aucune', 'Aucune'),
    ]
    preference_notification = models.CharField(
        max_length=10, 
        choices=PREFERENCE_NOTIF_CHOICES, 
        default='email',
        verbose_name="Préférence de notification"
    )

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Specialite(models.Model):
    """Spécialité médicale"""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la spécialité")
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True, help_text="Nom de l'icône ou classe CSS")
    
    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Cabinet(models.Model):
    """Cabinet médical"""
    nom = models.CharField(max_length=200, verbose_name="Nom du cabinet")
    
    adresse = models.TextField(verbose_name="Adresse")
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        verbose_name = "Cabinet"
        verbose_name_plural = "Cabinets"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} - {self.ville}"


class Professionnel(models.Model):
    """Professionnel de santé"""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255, verbose_name="Mot de passe (hashé)")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    
    numero_rpps = models.CharField(
        max_length=11, 
        unique=True, 
        verbose_name="Numéro RPPS",
        help_text="Répertoire Partagé des Professionnels de Santé"
    )
    specialite = models.ForeignKey(
        Specialite, 
        on_delete=models.PROTECT, 
        related_name='professionnels',
        verbose_name="Spécialité"
    )
    
    bio = models.TextField(blank=True, verbose_name="Biographie")
    photo_url = models.URLField(blank=True, verbose_name="URL de la photo")
    
    tarif_consultation = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Tarif de consultation (€)"
    )
    
    accepte_teleconsultation = models.BooleanField(default=False, verbose_name="Accepte la téléconsultation")
    
    STATUT_VALIDATION_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]
    statut_validation = models.CharField(
        max_length=15, 
        choices=STATUT_VALIDATION_CHOICES, 
        default='en_attente',
        verbose_name="Statut de validation"
    )
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    valide_par_admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='professionnels_valides',
        verbose_name="Validé par (Admin)",
        limit_choices_to={'is_staff': True}
    )
    
    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    
    cabinets = models.ManyToManyField(
        Cabinet,
        through='ProfessionnelCabinet',
        related_name='professionnels',
        verbose_name="Cabinets"
    )
    
    class Meta:
        verbose_name = "Professionnel"
        verbose_name_plural = "Professionnels"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"Dr {self.prenom} {self.nom} - {self.specialite.nom}"


class ProfessionnelCabinet(models.Model):
    """Association Professionnel-Cabinet"""
    professionnel = models.ForeignKey(Professionnel, on_delete=models.CASCADE)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    
    date_debut = models.DateField(default=timezone.now, verbose_name="Date de début")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    
    est_principal = models.BooleanField(default=False, verbose_name="Cabinet principal")
    
    class Meta:
        verbose_name = "Professionnel - Cabinet"
        verbose_name_plural = "Professionnels - Cabinets"
        unique_together = ['professionnel', 'cabinet']

    def __str__(self):
        return f"{self.professionnel} @ {self.cabinet}"


class MotifConsultation(models.Model):
    """Motif de consultation"""
    specialite = models.ForeignKey(
        Specialite, 
        on_delete=models.CASCADE, 
        related_name='motifs_consultation',
        verbose_name="Spécialité"
    )
    libelle = models.CharField(max_length=200, verbose_name="Libellé")
    duree_estimee = models.IntegerField(
        validators=[MinValueValidator(5)],
        verbose_name="Durée estimée (minutes)",
        help_text="Durée en minutes"
    )
    tarif = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Tarif (€)"
    )
    
    class Meta:
        verbose_name = "Motif de consultation"
        verbose_name_plural = "Motifs de consultation"
        ordering = ['specialite', 'libelle']
        unique_together = ['specialite', 'libelle']

    def __str__(self):
        return f"{self.libelle} ({self.specialite.nom}) - {self.duree_estimee}min"


class DisponibiliteHoraire(models.Model):
    """Disponibilité horaire"""
    professionnel = models.ForeignKey(
        Professionnel, 
        on_delete=models.CASCADE, 
        related_name='disponibilites'
    )
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    
    JOUR_SEMAINE_CHOICES = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]
    jour_semaine = models.IntegerField(choices=JOUR_SEMAINE_CHOICES, verbose_name="Jour de la semaine")
    
    heure_debut = models.TimeField(verbose_name="Heure de début")
    heure_fin = models.TimeField(verbose_name="Heure de fin")
    
    duree_creneau = models.IntegerField(
        validators=[MinValueValidator(5)],
        default=30,
        verbose_name="Durée du créneau (minutes)",
        help_text="Durée d'un créneau de rendez-vous en minutes"
    )
    
    class Meta:
        verbose_name = "Disponibilité horaire"
        verbose_name_plural = "Disponibilités horaires"
        ordering = ['professionnel', 'jour_semaine', 'heure_debut']

    def __str__(self):
        return f"{self.professionnel} - {self.get_jour_semaine_display()} {self.heure_debut}-{self.heure_fin}"


class RendezVous(models.Model):
    """Rendez-vous"""
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='rendez_vous',
        verbose_name="Patient"
    )
    professionnel = models.ForeignKey(
        Professionnel, 
        on_delete=models.CASCADE, 
        related_name='rendez_vous',
        verbose_name="Professionnel"
    )
    cabinet = models.ForeignKey(
        Cabinet, 
        on_delete=models.CASCADE, 
        related_name='rendez_vous',
        verbose_name="Cabinet"
    )
    motif_consultation = models.ForeignKey(
        MotifConsultation,
        on_delete=models.PROTECT,
        related_name='rendez_vous',
        verbose_name="Motif de consultation"
    )
    
    date = models.DateField(verbose_name="Date")
    heure_debut = models.TimeField(verbose_name="Heure de début")
    heure_fin = models.TimeField(verbose_name="Heure de fin")
    
    STATUT_CHOICES = [
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('termine', 'Terminé'),
        ('no_show', 'Patient absent'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='confirme')
    
    MODE_CHOICES = [
        ('presentiel', 'Présentiel'),
        ('teleconsultation', 'Téléconsultation'),
    ]
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='presentiel')
    
    notes_patient = models.TextField(blank=True, verbose_name="Notes du patient")
    notes_professionnel = models.TextField(blank=True, verbose_name="Notes du professionnel")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    date_annulation = models.DateTimeField(null=True, blank=True, verbose_name="Date d'annulation")
    
    rappel_envoye = models.BooleanField(default=False, verbose_name="Rappel envoyé")
    
    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['-date', '-heure_debut']
        indexes = [
            models.Index(fields=['date', 'professionnel']),
            models.Index(fields=['patient', 'date']),
        ]

    def __str__(self):
        return f"{self.patient} avec {self.professionnel} le {self.date} à {self.heure_debut}"


class Favoris(models.Model):
    """Favori"""
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='favoris',
        verbose_name="Patient"
    )
    professionnel = models.ForeignKey(
        Professionnel, 
        on_delete=models.CASCADE, 
        related_name='favoris',
        verbose_name="Professionnel"
    )
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    
    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        unique_together = ['patient', 'professionnel']
        ordering = ['-date_ajout']

    def __str__(self):
        return f"{self.patient} - Favori: {self.professionnel}"
