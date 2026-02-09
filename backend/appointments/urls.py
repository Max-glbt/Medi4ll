from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('check-admin/', views.check_admin, name='check-admin'),
    path('rendez-vous/', views.get_user_rendez_vous, name='user-rendez-vous'),
    path('rendez-vous/create/', views.create_rendez_vous, name='create-rendez-vous'),
    path('rendez-vous/professionnel/', views.professionnel_rendez_vous, name='professionnel-rendez-vous'),
    path('rendez-vous/<int:rdv_id>/statut/', views.update_rendez_vous_statut, name='update-rendez-vous-statut'),
    path('user/profile/', views.user_profile, name='user-profile'),
    path('specialites/', views.get_specialites, name='specialites'),
    path('professionnels/', views.get_professionnels, name='professionnels'),
    path('professionnels/<int:professionnel_id>/disponibilites/', views.professionnel_disponibilites, name='professionnel-disponibilites'),
    path('professionnels/manage/', views.professionnels_list_create, name='professionnels-manage'),
    path('professionnels/manage/<int:pk>/', views.professionnel_detail, name='professionnel-detail'),
    path('cabinets/', views.get_cabinets, name='cabinets'),
    path('admin/rendez-vous/', views.admin_rendez_vous, name='admin-rendez-vous'),
    path('admin/rendez-vous/<int:rdv_id>/', views.admin_rendez_vous, name='admin-rendez-vous-delete'),
    path('admin/clients/', views.admin_clients, name='admin-clients'),
    path('admin/clients/<int:client_id>/', views.admin_clients, name='admin-clients-delete'),
    path('professionnel/disponibilites/', views.manage_disponibilites, name='manage-disponibilites'),
    path('professionnel/disponibilites/<int:dispo_id>/', views.manage_disponibilite_detail, name='manage-disponibilite-detail'),
    path('professionnel/profile/', views.manage_professionnel_profile, name='manage-professionnel-profile'),
    path('professionnel/cabinets/', views.manage_professionnel_cabinets, name='manage-professionnel-cabinets'),
    path('professionnel/cabinets/<int:cabinet_id>/', views.manage_professionnel_cabinet_detail, name='manage-professionnel-cabinet-detail'),
]
