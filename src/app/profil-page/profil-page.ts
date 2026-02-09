import { Component, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Navbar } from '../navbar/navbar';
import { ConstantsService } from '../services/constants.service';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  date_naissance: string | null;
  sexe: string | null;
  telephone: string;
  telephone_urgence: string;
  adresse_complete: string;
  ville: string;
  code_postal: string;
  pays: string;
  numero_securite_sociale: string;
  preference_notification: string;
  statut: string;
}

interface RendezVous {
  id: number;
  professionnel: {
    id: number;
    nom: string;
    prenom: string;
    specialite: { nom: string };
  };
  cabinet: {
    nom: string;
    adresse: string;
    ville: string;
  } | null;
  date: string;
  heure_debut: string;
  heure_fin: string;
  statut: string;
  mode: string;
  notes_patient: string;
}

interface ProfessionnelProfile {
  id: number;
  nom: string;
  prenom: string;
  email: string;
  specialite: { id: number; nom: string; description: string };
  bio?: string;
  photo_url?: string;
  tarif_consultation: string;
  accepte_teleconsultation: boolean;
  cabinets?: Array<{
    id: number;
    nom: string;
    adresse: string;
    ville: string;
    code_postal: string;
    telephone: string;
  }>;
}

interface DisponibiliteHoraire {
  id: number;
  jour_semaine: number; 
  heure_debut: string;
  heure_fin: string;
  duree_creneau: number;
  cabinet: { id: number; nom: string };
}

interface Cabinet {
  id: number;
  nom: string;
  adresse: string;
  ville: string;
  code_postal: string;
  telephone: string;
}

@Component({
  selector: 'app-profil-page',
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './profil-page.html',
  styleUrl: './profil-page.css',
  standalone: true
})
export class ProfilPage implements OnInit {
  private apiUrl = '/api';
  
  user = signal<User | null>(null);
  isEditingProfile = signal(false);
  
  rendezVousPatient = signal<RendezVous[]>([]);
  rendezVousProfessionnel = signal<RendezVous[]>([]);
  isProfessionnel = signal(false);
  activeTab = signal<'profile' | 'rdv-patient' | 'rdv-pro'>('profile');

  professionnelProfile = signal<ProfessionnelProfile | null>(null);
  disponibilites = signal<DisponibiliteHoraire[]>([]);
  cabinets = signal<Cabinet[]>([]);
  newDispo = signal<{ cabinet_id: number | null; jour_semaine: number; heure_debut: string; heure_fin: string; duree_creneau: number }>({
    cabinet_id: null,
    jour_semaine: 0,
    heure_debut: '09:00',
    heure_fin: '17:00',
    duree_creneau: 30
  });
  editingDispoId = signal<number | null>(null);
  editingDispo = signal<{ cabinet_id: number; jour_semaine: number; heure_debut: string; heure_fin: string; duree_creneau: number } | null>(null);
  showAddDispoForm = signal(false);
  
  successMessage = signal('');
  errorMessage = signal('');
  isLoading = signal(false);

  constructor(
    private http: HttpClient,
    private constantsService: ConstantsService
  ) {}

  ngOnInit() {
    this.loadUserProfile();
    this.loadRendezVousPatient();
    this.checkIfProfessionnel();
  }

  loadUserProfile() {
    this.http.get<User>(`${this.apiUrl}/user/profile/`, { withCredentials: true }).subscribe({
      next: (data) => {
        this.user.set(data);
      },
      error: (err) => {
        console.error('Erreur chargement profil:', err);
        this.errorMessage.set('Impossible de charger le profil');
      }
    });
  }

  loadRendezVousPatient() {
    this.http.get<RendezVous[]>(`${this.apiUrl}/rendez-vous/`, { withCredentials: true }).subscribe({
      next: (data) => {
        this.rendezVousPatient.set(data);
      },
      error: (err) => {
        console.error('Erreur chargement rendez-vous patient:', err);
      }
    });
  }

  checkIfProfessionnel() {
    this.http.get<RendezVous[]>(`${this.apiUrl}/rendez-vous/professionnel/`, { withCredentials: true }).subscribe({
      next: (data) => {
        this.isProfessionnel.set(true);
        this.rendezVousProfessionnel.set(data);
        this.loadProfessionnelProfile();
        this.loadDisponibilitesProfessionnel();
        this.loadCabinets();
      },
      error: () => {
        this.isProfessionnel.set(false);
      }
    });
  }

  updateProfile() {
    if (!this.user()) return;
    
    this.isLoading.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    this.http.put<User>(`${this.apiUrl}/user/profile/`, this.user(), { withCredentials: true }).subscribe({
      next: (data) => {
        this.user.set(data);
        this.isEditingProfile.set(false);
        this.successMessage.set('Profil mis à jour avec succès');
        this.isLoading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        console.error('Erreur mise à jour profil:', err);
        this.errorMessage.set('Erreur lors de la mise à jour');
        this.isLoading.set(false);
      }
    });
  }

  updateRendezVousStatut(rdvId: number, nouveauStatut: string) {
    this.http.put(`${this.apiUrl}/rendez-vous/${rdvId}/statut/`, { statut: nouveauStatut }, { withCredentials: true }).subscribe({
      next: () => {
        this.http.get<RendezVous[]>(`${this.apiUrl}/rendez-vous/professionnel/`, { withCredentials: true }).subscribe({
          next: (data) => {
            this.rendezVousProfessionnel.set(data);
            this.successMessage.set('Statut mis à jour');
            setTimeout(() => this.successMessage.set(''), 3000);
          }
        });
      },
      error: (err) => {
        console.error('Erreur mise à jour statut:', err);
        this.errorMessage.set('Erreur lors de la mise à jour du statut');
      }
    });
  }

  getStatutBadgeClass(statut: string): string {
    return this.constantsService.getStatutBadgeClass(statut);
  }

  getStatutLabel(statut: string): string {
    return this.constantsService.getStatutLabel(statut);
  }

  formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('fr-FR', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    }).format(date);
  }

  joursLabels = Array.from({ length: 7 }, (_, i) => 
    new Intl.DateTimeFormat('fr-FR', { weekday: 'long' }).format(new Date(2024, 0, 1 + i))
  );

  getDisponibilitesByJour(jourIndex: number): DisponibiliteHoraire[] {
    return this.disponibilites().filter(d => d.jour_semaine === jourIndex).sort((a, b) => {
      return a.heure_debut.localeCompare(b.heure_debut);
    });
  }

  hasDisponibilitesForJour(jourIndex: number): boolean {
    return this.disponibilites().some(d => d.jour_semaine === jourIndex);
  }

  loadProfessionnelProfile() {
    this.http.get<ProfessionnelProfile>(`${this.apiUrl}/professionnel/profile/`, { withCredentials: true }).subscribe({
      next: (data) => this.professionnelProfile.set(data),
      error: (err) => console.error('Erreur profil professionnel:', err)
    });
  }

  saveProfessionnelSettings() {
    const prof = this.professionnelProfile();
    if (!prof) return;
    this.isLoading.set(true);
    this.http.put<ProfessionnelProfile>(`${this.apiUrl}/professionnel/profile/`, {
      tarif_consultation: prof.tarif_consultation,
      accepte_teleconsultation: prof.accepte_teleconsultation
    }, { withCredentials: true }).subscribe({
      next: (data) => {
        this.professionnelProfile.set(data);
        this.successMessage.set('Paramètres professionnels enregistrés');
        this.isLoading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        console.error('Erreur sauvegarde paramètres pro:', err);
        this.errorMessage.set('Erreur lors de l\'enregistrement des paramètres');
        this.isLoading.set(false);
      }
    });
  }

  loadDisponibilitesProfessionnel() {
    this.http.get<DisponibiliteHoraire[]>(`${this.apiUrl}/professionnel/disponibilites/`, { withCredentials: true }).subscribe({
      next: (data) => this.disponibilites.set(data),
      error: (err) => console.error('Erreur chargement disponibilités:', err)
    });
  }

  loadCabinets() {
    this.http.get<Cabinet[]>(`${this.apiUrl}/professionnel/cabinets/`, { withCredentials: true }).subscribe({
      next: (data) => this.cabinets.set(data),
      error: (err) => console.error('Erreur chargement cabinets:', err)
    });
  }

  newCabinet = signal<Cabinet>({ id: 0, nom: '', adresse: '', ville: '', code_postal: '', telephone: '' });

  addCabinet() {
    const cab = this.newCabinet();
    if (!cab.nom || !cab.adresse || !cab.ville || !cab.code_postal) {
      this.errorMessage.set('Veuillez remplir tous les champs du cabinet');
      return;
    }
    this.isLoading.set(true);
    this.http.post<Cabinet>(`${this.apiUrl}/professionnel/cabinets/`, {
      nom: cab.nom,
      adresse: cab.adresse,
      ville: cab.ville,
      code_postal: cab.code_postal,
      telephone: cab.telephone
    }, { withCredentials: true }).subscribe({
      next: () => {
        this.successMessage.set('Cabinet ajouté');
        this.newCabinet.set({ id: 0, nom: '', adresse: '', ville: '', code_postal: '', telephone: '' });
        this.loadCabinets();
        this.loadProfessionnelProfile();
        this.isLoading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        console.error('Erreur ajout cabinet:', err);
        this.errorMessage.set('Erreur lors de l\'ajout du cabinet');
        this.isLoading.set(false);
      }
    });
  }

  updateCabinet(cab: Cabinet) {
    this.isLoading.set(true);
    this.http.put<Cabinet>(`${this.apiUrl}/professionnel/cabinets/${cab.id}/`, {
      nom: cab.nom,
      adresse: cab.adresse,
      ville: cab.ville,
      code_postal: cab.code_postal,
      telephone: cab.telephone
    }, { withCredentials: true }).subscribe({
      next: () => {
        this.successMessage.set('Cabinet mis à jour');
        this.loadCabinets();
        this.loadProfessionnelProfile();
        this.isLoading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        console.error('Erreur mise à jour cabinet:', err);
        this.errorMessage.set('Erreur lors de la mise à jour du cabinet');
        this.isLoading.set(false);
      }
    });
  }

  deleteCabinet(id: number) {
    this.isLoading.set(true);
    this.http.delete(`${this.apiUrl}/professionnel/cabinets/${id}/`, { withCredentials: true }).subscribe({
      next: () => {
        this.successMessage.set('Cabinet supprimé');
        this.loadCabinets();
        this.loadProfessionnelProfile();
        this.isLoading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        console.error('Erreur suppression cabinet:', err);
        this.errorMessage.set('Erreur lors de la suppression du cabinet');
        this.isLoading.set(false);
      }
    });
  }

  addDisponibilite() {
    const dispo = this.newDispo();
    if (!dispo.cabinet_id) {
      this.errorMessage.set('Veuillez sélectionner un cabinet');
      return;
    }
    if (!this.validateHoraires(dispo.heure_debut, dispo.heure_fin)) {
      this.errorMessage.set('L\'heure de fin doit être après l\'heure de début');
      return;
    }
    this.isLoading.set(true);
    this.http.post<DisponibiliteHoraire>(`${this.apiUrl}/professionnel/disponibilites/`, {
      cabinet_id: dispo.cabinet_id,
      jour_semaine: dispo.jour_semaine,
      heure_debut: dispo.heure_debut,
      heure_fin: dispo.heure_fin,
      duree_creneau: dispo.duree_creneau
    }, { withCredentials: true }).subscribe({
      next: () => {
        this.successMessage.set('Disponibilité ajoutée avec succès');
        this.newDispo.set({
          cabinet_id: null,
          jour_semaine: 0,
          heure_debut: '09:00',
          heure_fin: '17:00',
          duree_creneau: 30
        });
        this.showAddDispoForm.set(false);
        this.loadDisponibilitesProfessionnel();
        this.isLoading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        console.error('Erreur ajout disponibilité:', err);
        this.errorMessage.set('Erreur lors de l\'ajout de la disponibilité');
        this.isLoading.set(false);
      }
    });
  }

  startEditDisponibilite(dispo: DisponibiliteHoraire) {
    this.editingDispoId.set(dispo.id);
    this.editingDispo.set({
      cabinet_id: dispo.cabinet.id,
      jour_semaine: dispo.jour_semaine,
      heure_debut: dispo.heure_debut,
      heure_fin: dispo.heure_fin,
      duree_creneau: dispo.duree_creneau
    });
  }

  cancelEditDisponibilite() {
    this.editingDispoId.set(null);
    this.editingDispo.set(null);
  }

  saveEditDisponibilite(id: number) {
    const dispo = this.editingDispo();
    if (!dispo) return;
    if (!this.validateHoraires(dispo.heure_debut, dispo.heure_fin)) {
      this.errorMessage.set('L\'heure de fin doit être après l\'heure de début');
      return;
    }
    this.isLoading.set(true);
    this.http.put<DisponibiliteHoraire>(`${this.apiUrl}/professionnel/disponibilites/${id}/`, {
      cabinet_id: dispo.cabinet_id,
      jour_semaine: dispo.jour_semaine,
      heure_debut: dispo.heure_debut,
      heure_fin: dispo.heure_fin,
      duree_creneau: dispo.duree_creneau
    }, { withCredentials: true }).subscribe({
      next: () => {
        this.successMessage.set('Disponibilité modifiée avec succès');
        this.cancelEditDisponibilite();
        this.loadDisponibilitesProfessionnel();
        this.isLoading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        console.error('Erreur modification disponibilité:', err);
        this.errorMessage.set('Erreur lors de la modification');
        this.isLoading.set(false);
      }
    });
  }

  validateHoraires(debut: string, fin: string): boolean {
    return debut < fin;
  }

  deleteDisponibilite(id: number) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette disponibilité ?')) {
      return;
    }
    this.isLoading.set(true);
    this.http.delete(`${this.apiUrl}/professionnel/disponibilites/${id}/`, { withCredentials: true }).subscribe({
      next: () => {
        this.successMessage.set('Disponibilité supprimée avec succès');
        this.loadDisponibilitesProfessionnel();
        this.isLoading.set(false);
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        console.error('Erreur suppression disponibilité:', err);
        this.errorMessage.set('Erreur lors de la suppression');
        this.isLoading.set(false);
      }
    });
  }
}
