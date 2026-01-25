from rest_framework import serializers
from .models import (
    User, Specialite, Cabinet, Professionnel, RendezVous,
    MotifConsultation, DisponibiliteHoraire, Favoris
)


class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialite
        fields = ['id', 'nom', 'description', 'icone']


class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ['id', 'nom', 'adresse', 'ville', 'code_postal', 'telephone', 'latitude', 'longitude']


class ProfessionnelSerializer(serializers.ModelSerializer):
    specialite = SpecialiteSerializer(read_only=True)
    cabinets = serializers.SerializerMethodField()
    
    class Meta:
        model = Professionnel
        fields = ['id', 'nom', 'prenom', 'email', 'specialite', 'bio', 'photo_url', 
                  'tarif_consultation', 'accepte_teleconsultation', 'statut_validation', 'cabinets']
    
    def get_cabinets(self, obj):
        # Récupère les cabinets via la relation ManyToMany
        cabinets = obj.cabinets.all()
        return CabinetSerializer(cabinets, many=True).data


class MotifConsultationSerializer(serializers.ModelSerializer):
    specialite = SpecialiteSerializer(read_only=True)
    
    class Meta:
        model = MotifConsultation
        fields = ['id', 'libelle', 'duree_estimee', 'tarif', 'specialite']


class RendezVousSerializer(serializers.ModelSerializer):
    professionnel = ProfessionnelSerializer(read_only=True)
    cabinet = CabinetSerializer(read_only=True)
    motif_consultation = MotifConsultationSerializer(read_only=True)
    
    class Meta:
        model = RendezVous
        fields = ['id', 'professionnel', 'cabinet', 'motif_consultation', 'date', 
                  'heure_debut', 'heure_fin', 'statut', 'mode', 'notes_patient', 
                  'rappel_envoye', 'date_creation']


class DisponibiliteHoraireSerializer(serializers.ModelSerializer):
    cabinet = CabinetSerializer(read_only=True)
    cabinet_id = serializers.IntegerField(write_only=True, required=True)
    
    class Meta:
        model = DisponibiliteHoraire
        fields = ['id', 'professionnel', 'cabinet', 'cabinet_id', 'jour_semaine', 'heure_debut', 'heure_fin', 'duree_creneau']
        read_only_fields = ['professionnel']
    
    def create(self, validated_data):
        cabinet_id = validated_data.pop('cabinet_id')
        cabinet = Cabinet.objects.get(id=cabinet_id)
        professionnel = self.context.get('professionnel')
        return DisponibiliteHoraire.objects.create(cabinet=cabinet, professionnel=professionnel, **validated_data)
    
    def update(self, instance, validated_data):
        cabinet_id = validated_data.pop('cabinet_id', None)
        if cabinet_id:
            instance.cabinet = Cabinet.objects.get(id=cabinet_id)
        for field in ['jour_semaine', 'heure_debut', 'heure_fin', 'duree_creneau']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'type_compte', 'date_naissance', 
                  'sexe', 'telephone', 'telephone_urgence', 'adresse_complete', 'ville', 
                  'code_postal', 'pays', 'numero_securite_sociale', 'preference_notification', 'statut']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Extraire le mot de passe et le type de compte
        password = validated_data.pop('password', None)
        type_compte = validated_data.pop('type_compte', 'client')
        user = User(**validated_data)
        user.type_compte = type_compte
        if password:
            user.set_password(password)
        user.save()
        return user
