from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Specialite, Cabinet, Professionnel, ProfessionnelCabinet,
    MotifConsultation, DisponibiliteHoraire, RendezVous, Favoris
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuration de l'admin pour le modèle User (Patient)"""
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('date_naissance', 'sexe', 'telephone', 'telephone_urgence',
                      'adresse_complete', 'ville', 'code_postal', 'pays',
                      'numero_securite_sociale', 'statut', 'preference_notification')
        }),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'statut', 'date_joined']
    list_filter = ['statut', 'date_joined', 'sexe']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telephone']


@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'icone']
    search_fields = ['nom']


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville', 'code_postal', 'telephone']
    list_filter = ['ville']
    search_fields = ['nom', 'ville', 'adresse']


@admin.register(Professionnel)
class ProfessionnelAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'specialite', 'email', 'statut_validation', 'date_inscription']
    list_filter = ['statut_validation', 'specialite', 'accepte_teleconsultation', 'date_inscription']
    search_fields = ['nom', 'prenom', 'email', 'numero_rpps']
    readonly_fields = ['date_inscription']


@admin.register(ProfessionnelCabinet)
class ProfessionnelCabinetAdmin(admin.ModelAdmin):
    list_display = ['professionnel', 'cabinet', 'date_debut', 'date_fin', 'est_principal']
    list_filter = ['est_principal', 'date_debut']
    search_fields = ['professionnel__nom', 'professionnel__prenom', 'cabinet__nom']


@admin.register(MotifConsultation)
class MotifConsultationAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'specialite', 'duree_estimee', 'tarif']
    list_filter = ['specialite']
    search_fields = ['libelle', 'specialite__nom']


@admin.register(DisponibiliteHoraire)
class DisponibiliteHoraireAdmin(admin.ModelAdmin):
    list_display = ['professionnel', 'cabinet', 'jour_semaine', 'heure_debut', 'heure_fin', 'duree_creneau']
    list_filter = ['jour_semaine', 'cabinet']
    search_fields = ['professionnel__nom', 'professionnel__prenom', 'cabinet__nom']


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ['date', 'heure_debut', 'patient', 'professionnel', 'cabinet', 'statut', 'mode']
    list_filter = ['statut', 'mode', 'date', 'professionnel__specialite']
    search_fields = ['patient__username', 'patient__first_name', 'patient__last_name',
                    'professionnel__nom', 'professionnel__prenom']
    readonly_fields = ['date_creation', 'date_modification']
    date_hierarchy = 'date'


@admin.register(Favoris)
class FavorisAdmin(admin.ModelAdmin):
    list_display = ['patient', 'professionnel', 'date_ajout']
    list_filter = ['date_ajout']
    search_fields = ['patient__username', 'professionnel__nom', 'professionnel__prenom']
    readonly_fields = ['date_ajout']
