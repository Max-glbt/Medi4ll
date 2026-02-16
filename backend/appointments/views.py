from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from datetime import datetime, timedelta, time as datetime_time
from .models import (
    User, RendezVous, Professionnel, Cabinet, Specialite, 
    DisponibiliteHoraire, MotifConsultation, ProfessionnelCabinet
)
from .serializers import (
    RendezVousSerializer, ProfessionnelSerializer, 
    CabinetSerializer, SpecialiteSerializer, UserSerializer, 
    DisponibiliteHoraireSerializer
)



@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_user(request):
    """Inscription d'un nouvel utilisateur"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        if request.data.get('type_compte') == 'professionnel' and request.data.get('specialite_id'):
            try:
                specialite = Specialite.objects.get(id=request.data.get('specialite_id'))
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
                    statut_validation='en_attente'
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
                'last_name': user.last_name,
                'type_compte': user.type_compte
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_user(request):
    """Connexion d'un utilisateur"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username et password requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return Response({
            'message': 'Connexion réussie',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'type_compte': user.type_compte,
                'is_admin': user.is_admin
            }
        })
    else:
        return Response(
            {'error': 'Identifiants invalides'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def logout_user(request):
    """Déconnexion d'un utilisateur"""
    logout(request)
    return Response({'message': 'Déconnexion réussie'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_admin(request):
    """Vérifie si l'utilisateur connecté est administrateur"""
    return Response({
        'is_admin': request.user.is_admin,
        'username': request.user.username
    })



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
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
@permission_classes([AllowAny])
def get_specialites(request):
    """Liste toutes les spécialités médicales"""
    specialites = Specialite.objects.all()
    serializer = SpecialiteSerializer(specialites, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_cabinets(request):
    """Liste tous les cabinets médicaux"""
    cabinets = Cabinet.objects.all()
    serializer = CabinetSerializer(cabinets, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_professionnels(request):
    """
    Liste tous les professionnels avec filtres optionnels
    Paramètres :
    - specialite : ID de la spécialité
    - ville : Nom de la ville
    - nom : Recherche dans nom/prenom
    - tarif_max : Prix maximum
    """
    professionnels = Professionnel.objects.filter(statut_validation='valide')
    
    specialite_id = request.GET.get('specialite')
    ville = request.GET.get('ville')
    nom = request.GET.get('nom')
    tarif_max = request.GET.get('tarif_max')
    
    if specialite_id:
        professionnels = professionnels.filter(specialite_id=specialite_id)
    
    if ville:
        professionnels = professionnels.filter(
            cabinets__ville__icontains=ville
        ).distinct()
    
    if nom:
        professionnels = professionnels.filter(
            Q(nom__icontains=nom) | Q(prenom__icontains=nom)
        )
    
    if tarif_max:
        try:
            professionnels = professionnels.filter(tarif_consultation__lte=float(tarif_max))
        except ValueError:
            pass
    
    serializer = ProfessionnelSerializer(professionnels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def professionnel_disponibilites(request, professionnel_id):
    """Récupère les disponibilités d'un professionnel"""
    try:
        professionnel = Professionnel.objects.get(id=professionnel_id)
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Professionnel non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    disponibilites = DisponibiliteHoraire.objects.filter(professionnel=professionnel)
    serializer = DisponibiliteHoraireSerializer(disponibilites, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_rendez_vous(request):
    """Liste les rendez-vous du patient connecté"""
    rendez_vous = RendezVous.objects.filter(patient=request.user).order_by('-date', '-heure_debut')
    
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    try:
        page = int(page)
        page_size = int(page_size)
        start = (page - 1) * page_size
        end = start + page_size
        
        total = rendez_vous.count()
        rendez_vous_page = rendez_vous[start:end]
        
        serializer = RendezVousSerializer(rendez_vous_page, many=True)
        return Response({
            'results': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
    except ValueError:
        serializer = RendezVousSerializer(rendez_vous, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_rendez_vous(request):
    """Crée un nouveau rendez-vous"""
    try:
        professionnel = Professionnel.objects.get(id=request.data.get('professionnel_id'))
        cabinet = Cabinet.objects.get(id=request.data.get('cabinet_id'))
        
        motif_consultation = None
        if request.data.get('motif_consultation_id'):
            motif_consultation = MotifConsultation.objects.get(id=request.data.get('motif_consultation_id'))
        
        rdv = RendezVous.objects.create(
            patient=request.user,
            professionnel=professionnel,
            cabinet=cabinet,
            motif_consultation=motif_consultation,
            date=request.data.get('date'),
            heure_debut=request.data.get('heure_debut'),
            heure_fin=request.data.get('heure_fin'),
            mode=request.data.get('mode', 'presentiel'),
            notes_patient=request.data.get('notes_patient', ''),
            statut='confirme'
        )
        
        serializer = RendezVousSerializer(rdv)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except (Professionnel.DoesNotExist, Cabinet.DoesNotExist, MotifConsultation.DoesNotExist) as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_rendez_vous_statut(request, rdv_id):
    """Modifie le statut d'un rendez-vous (patient ou professionnel)"""
    try:
        rdv = RendezVous.objects.get(id=rdv_id)
        
        if request.user != rdv.patient and not hasattr(request.user, 'professionnel'):
            return Response(
                {'error': 'Non autorisé'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        nouveau_statut = request.data.get('statut')
        if nouveau_statut in ['confirme', 'annule', 'termine', 'no_show']:
            rdv.statut = nouveau_statut
            if nouveau_statut == 'annule':
                rdv.date_annulation = datetime.now()
            rdv.save()
            
            serializer = RendezVousSerializer(rdv)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Statut invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except RendezVous.DoesNotExist:
        return Response(
            {'error': 'Rendez-vous non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def professionnel_rendez_vous(request):
    """Liste les rendez-vous reçus par le professionnel connecté"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
        rendez_vous = RendezVous.objects.filter(professionnel=professionnel).order_by('-date', '-heure_debut')
        serializer = RendezVousSerializer(rendez_vous, many=True)
        return Response(serializer.data)
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Professionnel non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def manage_professionnel_profile(request):
    """Récupère ou modifie le profil professionnel"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
        
        if request.method == 'GET':
            serializer = ProfessionnelSerializer(professionnel)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = ProfessionnelSerializer(professionnel, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Professionnel non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_disponibilites(request):
    """Gère les disponibilités horaires du professionnel"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
        
        if request.method == 'GET':
            disponibilites = DisponibiliteHoraire.objects.filter(professionnel=professionnel)
            serializer = DisponibiliteHoraireSerializer(disponibilites, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = DisponibiliteHoraireSerializer(
                data=request.data, 
                context={'professionnel': professionnel}
            )
            if serializer.is_valid():
                serializer.save(professionnel=professionnel)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Professionnel non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_disponibilite_detail(request, dispo_id):
    """Gère une disponibilité horaire spécifique"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
        disponibilite = DisponibiliteHoraire.objects.get(id=dispo_id, professionnel=professionnel)
        
        if request.method == 'GET':
            serializer = DisponibiliteHoraireSerializer(disponibilite)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = DisponibiliteHoraireSerializer(disponibilite, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            disponibilite.delete()
            return Response({'message': 'Disponibilité supprimée'}, status=status.HTTP_204_NO_CONTENT)
            
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Professionnel non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except DisponibiliteHoraire.DoesNotExist:
        return Response(
            {'error': 'Disponibilité non trouvée'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manage_professionnel_cabinets(request):
    """Gère les cabinets du professionnel"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
        
        if request.method == 'GET':
            cabinets = professionnel.cabinets.all()
            serializer = CabinetSerializer(cabinets, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            cabinet_id = request.data.get('cabinet_id')
            if cabinet_id:
                try:
                    cabinet = Cabinet.objects.get(id=cabinet_id)
                    professionnel.cabinets.add(cabinet)
                    return Response({'message': 'Cabinet ajouté'}, status=status.HTTP_201_CREATED)
                except Cabinet.DoesNotExist:
                    return Response(
                        {'error': 'Cabinet non trouvé'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                serializer = CabinetSerializer(data=request.data)
                if serializer.is_valid():
                    cabinet = serializer.save()
                    professionnel.cabinets.add(cabinet)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Professionnel non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def manage_professionnel_cabinet_detail(request, cabinet_id):
    """Retire un cabinet de la liste du professionnel"""
    try:
        professionnel = Professionnel.objects.get(email=request.user.email)
        cabinet = Cabinet.objects.get(id=cabinet_id)
        
        professionnel.cabinets.remove(cabinet)
        return Response({'message': 'Cabinet retiré'}, status=status.HTTP_204_NO_CONTENT)
        
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Professionnel non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Cabinet.DoesNotExist:
        return Response(
            {'error': 'Cabinet non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET', 'POST'])
@csrf_exempt
def professionnels_list_create(request):
    """Liste tous les professionnels ou crée un nouveau professionnel - Réservé aux admins"""
    if not request.user.is_authenticated or not request.user.is_admin:
        return Response(
            {'error': 'Accès réservé aux administrateurs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        professionnels = Professionnel.objects.all()
        serializer = ProfessionnelSerializer(professionnels, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProfessionnelSerializer(data=request.data)
        if serializer.is_valid():
            professionnel = serializer.save()
            return Response(
                ProfessionnelSerializer(professionnel).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def professionnel_detail(request, pk):
    """Récupère, modifie ou supprime un professionnel - Réservé aux admins"""
    if not request.user.is_authenticated or not request.user.is_admin:
        return Response(
            {'error': 'Accès réservé aux administrateurs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        professionnel = Professionnel.objects.get(pk=pk)
    except Professionnel.DoesNotExist:
        return Response(
            {'error': 'Professionnel non trouvé'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
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
        return Response(
            {'message': 'Professionnel supprimé'}, 
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def admin_rendez_vous(request, rdv_id=None):
    """Gère tous les rendez-vous (admin)"""
    if not request.user.is_admin:
        return Response(
            {'error': 'Accès réservé aux administrateurs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        rendez_vous = RendezVous.objects.all().order_by('-date', '-heure_debut')
        serializer = RendezVousSerializer(rendez_vous, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE' and rdv_id:
        try:
            rdv = RendezVous.objects.get(id=rdv_id)
            rdv.delete()
            return Response(
                {'message': 'Rendez-vous supprimé'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except RendezVous.DoesNotExist:
            return Response(
                {'error': 'Rendez-vous non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def admin_clients(request, client_id=None):
    """Gère tous les clients (admin)"""
    if not request.user.is_admin:
        return Response(
            {'error': 'Accès réservé aux administrateurs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        clients = User.objects.filter(type_compte='client')
        serializer = UserSerializer(clients, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE' and client_id:
        try:
            client = User.objects.get(id=client_id, type_compte='client')
            client.delete()
            return Response(
                {'message': 'Client supprimé'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Client non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )
