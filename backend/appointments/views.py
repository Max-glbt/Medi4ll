from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import RendezVous, Professionnel, Cabinet, Specialite
from .serializers import (
    RendezVousSerializer, ProfessionnelSerializer, 
    CabinetSerializer, SpecialiteSerializer, UserSerializer, DisponibiliteHoraireSerializer
)


# CRUD Professionnels
@api_view(['GET', 'POST'])
@csrf_exempt
def professionnels_list_create(request):
    """Liste tous les professionnels ou crée un nouveau professionnel - Réservé aux admins"""
    # Vérifier que l'utilisateur est admin
    if not request.user.is_authenticated or not request.user.is_admin:
        return Response({'error': 'Accès réservé aux administrateurs'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        professionnels = Professionnel.objects.all()
        serializer = ProfessionnelSerializer(professionnels, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()
        serializer = ProfessionnelSerializer(data=data)
        if serializer.is_valid():
            professionnel = serializer.save()
            return Response(ProfessionnelSerializer(professionnel).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def professionnel_detail(request, pk):
    """Récupère, modifie ou supprime un professionnel - Réservé aux admins"""
    # Vérifier que l'utilisateur est admin
    if not request.user.is_authenticated or not request.user.is_admin:
        return Response({'error': 'Accès réservé aux administrateurs'}, status=status.HTTP_403_FORBIDDEN)
    try:
        professionnel = Professionnel.objects.get(pk=pk)
    except Professionnel.DoesNotExist:
        return Response({'error': 'Professionnel non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProfessionnelSerializer(professionnel)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProfessionnelSerializer(professionnel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        professionnel.delete()
        return Response({'message': 'Professionnel supprimé'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_user(request):
    """Inscription d'un nouvel utilisateur"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Si c'est un professionnel, créer automatiquement l'objet Professionnel
        if request.data.get('type_compte') == 'professionnel' and request.data.get('specialite_id'):
            try:
                specialite = Specialite.objects.get(id=request.data.get('specialite_id'))
                # Générer un numero_rpps unique basé sur l'ID et le timestamp
                import time
                numero_rpps = f"TEMP{user.id}{int(time.time()) % 1000000}"
                
                Professionnel.objects.create(
                    nom=user.last_name,
                    prenom=user.first_name,
                    email=user.email,
                    specialite=specialite,
                    numero_rpps=numero_rpps,
                    telephone='',
                    password_hash='',
                    bio='',
                    tarif_consultation=50,
                    accepte_teleconsultation=False,
                    statut_validation='EN_ATTENTE'
                )
            except Specialite.DoesNotExist:
                pass
        
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_user(request):
    """Authentification d'un utilisateur avec session"""
    # Accepter soit l'email, soit le username
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Si email fourni, retrouver le username correspondant
    from .models import User
    if email and not username:
        try:
            u = User.objects.get(email=email)
            username = u.username
        except User.DoesNotExist:
            username = None
    
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)  # Crée la session
        return Response({
            'message': 'Connexion réussie',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Identifiants incorrects'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def logout_user(request):
    """Déconnexion de l'utilisateur"""
    logout(request)
    return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def check_admin(request):
    """Vérifie si l'utilisateur connecté est admin"""
    return Response({'is_admin': request.user.is_admin}, status=status.HTTP_200_OK)


# Admin - Gestion des rendez-vous
@api_view(['GET', 'DELETE'])
@csrf_exempt
def admin_rendez_vous(request, rdv_id=None):
    """Liste ou supprime tous les rendez-vous - Réservé aux admins"""
    if not request.user.is_authenticated or not request.user.is_admin:
        return Response({'error': 'Accès réservé aux administrateurs'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        rendez_vous = RendezVous.objects.all().order_by('-date', '-heure_debut')
        serializer = RendezVousSerializer(rendez_vous, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        try:
            rdv = RendezVous.objects.get(id=rdv_id)
            rdv.delete()
            return Response({'message': 'Rendez-vous supprimé'}, status=status.HTTP_204_NO_CONTENT)
        except RendezVous.DoesNotExist:
            return Response({'error': 'Rendez-vous non trouvé'}, status=status.HTTP_404_NOT_FOUND)


# Admin - Gestion des clients
@api_view(['GET', 'DELETE'])
@csrf_exempt
def admin_clients(request, client_id=None):
    """Liste ou supprime tous les clients - Réservé aux admins"""
    if not request.user.is_authenticated or not request.user.is_admin:
        return Response({'error': 'Accès réservé aux administrateurs'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        from .models import User
        clients = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(clients, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        try:
            from .models import User
            client = User.objects.get(id=client_id)
            if client.is_admin:
                return Response({'error': 'Impossible de supprimer un administrateur'}, status=status.HTTP_400_BAD_REQUEST)
            client.delete()
            return Response({'message': 'Client supprimé'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'Client non trouvé'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def get_user_rendez_vous(request):
    """Récupère tous les rendez-vous de l'utilisateur connecté"""
    print(f"DEBUG - User authentifié: {request.user}")
    print(f"DEBUG - User is_authenticated: {request.user.is_authenticated}")
    rendez_vous = RendezVous.objects.filter(patient=request.user).order_by('date', 'heure_debut')
    print(f"DEBUG - Nombre de rendez-vous trouvés: {rendez_vous.count()}")
    serializer = RendezVousSerializer(rendez_vous, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def get_specialites(request):
    """Liste toutes les spécialités"""
    specialites = Specialite.objects.all()
    serializer = SpecialiteSerializer(specialites, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def get_professionnels(request):
    """Liste tous les professionnels (validation supprimée)"""
    professionnels = Professionnel.objects.all()
    serializer = ProfessionnelSerializer(professionnels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def get_cabinets(request):
    """Liste tous les cabinets"""
    cabinets = Cabinet.objects.all()
    serializer = CabinetSerializer(cabinets, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_rendez_vous(request):
    """Crée un nouveau rendez-vous"""
    from datetime import datetime, time
    from .models import MotifConsultation
    from django.db import transaction
    
    try:
        professionnel_id = request.data.get('professionnel_id')
        cabinet_id = request.data.get('cabinet_id')
        date_str = request.data.get('date')
        heure_debut_str = request.data.get('heure_debut')
        mode_input = request.data.get('mode', 'PRESENTIEL')
        notes_patient = request.data.get('notes_patient', '')
        motif_id = request.data.get('motif_consultation_id')
        
        # Validation
        if not all([professionnel_id, date_str, heure_debut_str, cabinet_id]):
            return Response(
                {'error': 'Données manquantes (professionnel, cabinet, date, heure)'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les objets
        try:
            professionnel = Professionnel.objects.get(id=professionnel_id)
        except Professionnel.DoesNotExist:
            return Response(
                {'error': 'Professionnel non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            cabinet = Cabinet.objects.get(id=cabinet_id)
        except Cabinet.DoesNotExist:
            return Response(
                {'error': 'Cabinet non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Parser la date et l'heure
        date_rdv = datetime.strptime(date_str, '%Y-%m-%d').date()
        heure_debut = datetime.strptime(heure_debut_str, '%H:%M').time()
        
        # Calculer l'heure de fin (30 minutes après)
        heure_debut_dt = datetime.combine(date_rdv, heure_debut)
        from datetime import timedelta
        heure_fin_dt = heure_debut_dt + timedelta(minutes=30)
        heure_fin = heure_fin_dt.time()
        
        # Mode
        mode = 'presentiel' if str(mode_input).upper() == 'PRESENTIEL' else 'teleconsultation'

        # Motif de consultation: utiliser l'ID fourni ou créer/récupérer un motif générique
        motif = None
        if motif_id:
            try:
                motif = MotifConsultation.objects.get(id=motif_id)
            except MotifConsultation.DoesNotExist:
                motif = None
        if motif is None:
            motif, _ = MotifConsultation.objects.get_or_create(
                specialite=professionnel.specialite,
                libelle='Consultation',
                defaults={
                    'duree_estimee': 30,
                    'tarif': professionnel.tarif_consultation
                }
            )

        # Empêcher la double réservation pour ce créneau et ce professionnel
        from django.db.models import Q
        overlap_exists = RendezVous.objects.filter(
            professionnel=professionnel,
            date=date_rdv
        ).exclude(statut='annule').filter(
            Q(heure_debut__lt=heure_fin) & Q(heure_fin__gt=heure_debut)
        ).exists()
        if overlap_exists:
            return Response({'error': 'Créneau indisponible'}, status=status.HTTP_409_CONFLICT)

        # Empêcher plusieurs rendez-vous à venir avec le même professionnel pour ce patient
        today = datetime.today().date()
        existing_future = RendezVous.objects.filter(
            patient=request.user,
            professionnel=professionnel,
            date__gte=today
        ).exclude(statut='annule').exists()
        if existing_future:
            return Response({'error': 'Vous avez déjà un rendez-vous à venir avec ce professionnel'}, status=status.HTTP_409_CONFLICT)

        # Créer le rendez-vous en transaction
        with transaction.atomic():
            rendez_vous = RendezVous.objects.create(
                patient=request.user,
                professionnel=professionnel,
                cabinet=cabinet,
                motif_consultation=motif,
                date=date_rdv,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                statut='confirme',
                mode=mode,
                notes_patient=notes_patient
            )
        
        serializer = RendezVousSerializer(rendez_vous)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def user_profile(request):
    """Récupère ou modifie le profil de l'utilisateur connecté"""
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def professionnel_rendez_vous(request):
    """Récupère tous les rendez-vous pour un professionnel de santé"""
    try:
        # Trouver le professionnel associé à cet utilisateur
        professionnel = Professionnel.objects.get(email=request.user.email)
        rendez_vous = RendezVous.objects.filter(professionnel=professionnel).order_by('date', 'heure_debut')
        serializer = RendezVousSerializer(rendez_vous, many=True)
        return Response(serializer.data)
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Aucun professionnel associé à cet utilisateur'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def professionnel_disponibilites(request, professionnel_id):
    """Liste les disponibilités ou renvoie les créneaux disponibles pour une date"""
    try:
        professionnel = Professionnel.objects.get(id=professionnel_id)
    except Professionnel.DoesNotExist:
        return Response({'error': 'Professionnel non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    date_str = request.GET.get('date')
    cabinet_id = request.GET.get('cabinet_id')
    from datetime import datetime, timedelta
    if not date_str:
        # Retourner les disponibilités brutes
        from .models import DisponibiliteHoraire
        qs = DisponibiliteHoraire.objects.filter(professionnel=professionnel)
        if cabinet_id:
            qs = qs.filter(cabinet_id=cabinet_id)
        dispos = qs
        serializer = DisponibiliteHoraireSerializer(dispos, many=True)
        return Response(serializer.data)

    # Calculer les créneaux disponibles pour la date
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Format de date invalide (attendu YYYY-MM-DD)'}, status=status.HTTP_400_BAD_REQUEST)

    jour_idx = date_obj.weekday()  # 0 = lundi, ... 6 = dimanche
    from .models import DisponibiliteHoraire
    qs = DisponibiliteHoraire.objects.filter(professionnel=professionnel, jour_semaine=jour_idx)
    if cabinet_id:
        qs = qs.filter(cabinet_id=cabinet_id)
    dispos = qs

    # Récupérer les RDV existants ce jour-là (hors annulés)
    rdvs = RendezVous.objects.filter(professionnel=professionnel, date=date_obj).exclude(statut='annule')

    slots = []
    for dispo in dispos:
        start_dt = datetime.combine(date_obj, dispo.heure_debut)
        end_dt = datetime.combine(date_obj, dispo.heure_fin)
        step = timedelta(minutes=dispo.duree_creneau)
        t = start_dt
        while t + step <= end_dt:
            # Vérifier si le créneau chevauche un RDV existant
            overlap = False
            for rdv in rdvs:
                rdv_start = datetime.combine(date_obj, rdv.heure_debut)
                rdv_end = datetime.combine(date_obj, rdv.heure_fin)
                if rdv_start <= t < rdv_end:
                    overlap = True
                    break
            if not overlap:
                slots.append(t.strftime('%H:%M'))
            t = t + step

    # Nettoyer et trier
    slots = sorted(list(set(slots)))
    return Response({'slots': slots})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def manage_disponibilites(request):
    """Gestion des disponibilités par le professionnel connecté"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
    except Professionnel.DoesNotExist:
        return Response({'error': 'Aucun professionnel associé à cet utilisateur'}, status=status.HTTP_403_FORBIDDEN)

    from .models import DisponibiliteHoraire
    if request.method == 'GET':
        dispos = DisponibiliteHoraire.objects.filter(professionnel=professionnel)
        serializer = DisponibiliteHoraireSerializer(dispos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DisponibiliteHoraireSerializer(data=request.data, context={'professionnel': professionnel})
        if serializer.is_valid():
            dispo = serializer.save()
            return Response(DisponibiliteHoraireSerializer(dispo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def manage_disponibilite_detail(request, dispo_id):
    """Modification/Suppression d'une disponibilité par le professionnel connecté"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
    except Professionnel.DoesNotExist:
        return Response({'error': 'Aucun professionnel associé à cet utilisateur'}, status=status.HTTP_403_FORBIDDEN)

    from .models import DisponibiliteHoraire
    try:
        dispo = DisponibiliteHoraire.objects.get(id=dispo_id, professionnel=professionnel)
    except DisponibiliteHoraire.DoesNotExist:
        return Response({'error': 'Disponibilité non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = DisponibiliteHoraireSerializer(dispo, data=request.data, partial=True, context={'professionnel': professionnel})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        dispo.delete()
        return Response({'message': 'Disponibilité supprimée'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def manage_professionnel_profile(request):
    """Permet au professionnel connecté de consulter/modifier son profil (tarif, téléconsultation)"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
    except Professionnel.DoesNotExist:
        return Response({'error': 'Aucun professionnel associé à cet utilisateur'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        return Response(ProfessionnelSerializer(professionnel).data)
    elif request.method == 'PUT':
        serializer = ProfessionnelSerializer(professionnel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def manage_professionnel_cabinets(request):
    """Permet au professionnel connecté de lister/ajouter ses cabinets"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
    except Professionnel.DoesNotExist:
        return Response({'error': 'Aucun professionnel associé à cet utilisateur'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        cabinets = professionnel.cabinets.all()
        return Response(CabinetSerializer(cabinets, many=True).data)
    elif request.method == 'POST':
        # Créer un nouveau cabinet et l'associer
        serializer = CabinetSerializer(data=request.data)
        if serializer.is_valid():
            cabinet = serializer.save()
            from .models import ProfessionnelCabinet
            ProfessionnelCabinet.objects.create(professionnel=professionnel, cabinet=cabinet, est_principal=False)
            return Response(CabinetSerializer(cabinet).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def manage_professionnel_cabinet_detail(request, cabinet_id):
    """Permet au professionnel connecté de modifier/supprimer l'association d'un cabinet"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
    except Professionnel.DoesNotExist:
        return Response({'error': 'Aucun professionnel associé à cet utilisateur'}, status=status.HTTP_403_FORBIDDEN)

    try:
        cabinet = professionnel.cabinets.get(id=cabinet_id)
    except Cabinet.DoesNotExist:
        return Response({'error': 'Cabinet non associé'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CabinetSerializer(cabinet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Supprimer l'association; si plus aucun pro lié, supprimer le cabinet
        from .models import ProfessionnelCabinet
        ProfessionnelCabinet.objects.filter(professionnel=professionnel, cabinet=cabinet).delete()
        if cabinet.professionnels.count() == 0:
            cabinet.delete()
            return Response({'message': 'Cabinet et association supprimés'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Association supprimée'}, status=status.HTTP_204_NO_CONTENT)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_rendez_vous_statut(request, rdv_id):
    """Modifie le statut d'un rendez-vous (pour les professionnels)"""
    try:
        rendez_vous = RendezVous.objects.get(id=rdv_id)
        
        # Vérifier que l'utilisateur est le professionnel du rendez-vous
        professionnel = Professionnel.objects.get(email=request.user.email)
        if rendez_vous.professionnel != professionnel:
            return Response(
                {'error': 'Non autorisé'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        nouveau_statut = request.data.get('statut')
        if nouveau_statut:
            rendez_vous.statut = nouveau_statut
            rendez_vous.save()
            serializer = RendezVousSerializer(rendez_vous)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Statut manquant'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    except RendezVous.DoesNotExist:
        return Response(
            {'error': 'Rendez-vous non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Aucun professionnel associé'}, 
            status=status.HTTP_403_FORBIDDEN
        )

