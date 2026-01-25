import { Component, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Navbar } from '../navbar/navbar';

interface Professionnel {
  id?: number;
  nom: string;
  prenom: string;
  email: string;
  specialite: number;
  bio: string;
  tarif_consultation: number;
  accepte_teleconsultation: boolean;
  statut_validation: string;
}

interface Specialite {
  id: number;
  nom: string;
}

interface RendezVous {
  id: number;
  patient: {
    id: number;
    username: string;
    email: string;
  };
  professionnel: {
    id: number;
    nom: string;
    prenom: string;
    specialite: { nom: string };
  };
  date: string;
  heure_debut: string;
  heure_fin: string;
  statut: string;
  mode: string;
}

interface Client {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  type_compte: string;
  telephone: string;
  ville: string;
  statut: string;
  is_admin: boolean;
}

type TabType = 'professionnels' | 'rendez-vous' | 'clients';

@Component({
  selector: 'app-admin-page',
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './admin-page.html',
  styleUrl: './admin-page.css',
  standalone: true
})
export class AdminPage implements OnInit {
  private apiUrl = '/api';
  
  // Onglet actif
  activeTab = signal<TabType>('professionnels');
  
  // Professionnels
  professionnels = signal<Professionnel[]>([]);
  specialites = signal<Specialite[]>([]);
  isEditingProf = signal(false);
  currentProfessionnel = signal<Professionnel>({
    nom: '',
    prenom: '',
    email: '',
    specialite: 0,
    bio: '',
    tarif_consultation: 0,
    accepte_teleconsultation: false,
    statut_validation: 'VALIDE'
  });
  
  // Rendez-vous
  rendezVous = signal<RendezVous[]>([]);
  
  // Clients
  clients = signal<Client[]>([]);
  
  // Pagination
  pageProfessionnels = signal(1);
  pageRendezVous = signal(1);
  pageClients = signal(1);
  parPage = 20;
  
  successMessage = signal('');
  errorMessage = signal('');

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadProfessionnels();
    this.loadSpecialites();
    this.loadRendezVous();
    this.loadClients();
  }

  // Gestion des onglets
  setTab(tab: TabType) {
    this.activeTab.set(tab);
    this.isEditingProf.set(false);
  }

  loadProfessionnels() {
    this.http.get<Professionnel[]>(`${this.apiUrl}/professionnels/manage/`, {
      withCredentials: true
    }).subscribe({
      next: (data) => this.professionnels.set(data),
      error: (err) => {
        console.error('Erreur chargement:', err);
        this.errorMessage.set('Erreur de chargement des professionnels');
      }
    });
  }

  loadSpecialites() {
    this.http.get<Specialite[]>(`${this.apiUrl}/specialites/`, {
      withCredentials: true
    }).subscribe({
      next: (data) => this.specialites.set(data)
    });
  }

  loadRendezVous() {
    this.http.get<RendezVous[]>(`${this.apiUrl}/admin/rendez-vous/`, {
      withCredentials: true
    }).subscribe({
      next: (data) => this.rendezVous.set(data),
      error: (err) => {
        console.error('Erreur chargement rendez-vous:', err);
        this.errorMessage.set('Erreur de chargement des rendez-vous');
      }
    });
  }

  loadClients() {
    this.http.get<Client[]>(`${this.apiUrl}/admin/clients/`, {
      withCredentials: true
    }).subscribe({
      next: (data) => this.clients.set(data),
      error: (err) => {
        console.error('Erreur chargement clients:', err);
        this.errorMessage.set('Erreur de chargement des clients');
      }
    });
  }

  newProfessionnel() {
    this.currentProfessionnel.set({
      nom: '',
      prenom: '',
      email: '',
      specialite: 0,
      bio: '',
      tarif_consultation: 50,
      accepte_teleconsultation: false,
      statut_validation: 'VALIDE'
    });
    this.isEditingProf.set(true);
  }

  editProfessionnel(prof: Professionnel) {
    this.currentProfessionnel.set({ ...prof });
    this.isEditingProf.set(true);
  }

  saveProfessionnel() {
    const prof = this.currentProfessionnel();
    
    if (prof.id) {
      // Update
      this.http.put(`${this.apiUrl}/professionnels/manage/${prof.id}/`, prof, {
        withCredentials: true
      }).subscribe({
        next: () => {
          this.successMessage.set('Professionnel modifié');
          this.loadProfessionnels();
          this.isEditingProf.set(false);
          setTimeout(() => this.successMessage.set(''), 3000);
        },
        error: (err) => {
          this.errorMessage.set('Erreur de modification');
          console.error(err);
        }
      });
    } else {
      // Create
      this.http.post(`${this.apiUrl}/professionnels/manage/`, prof, {
        withCredentials: true
      }).subscribe({
        next: () => {
          this.successMessage.set('Professionnel créé');
          this.loadProfessionnels();
          this.isEditingProf.set(false);
          setTimeout(() => this.successMessage.set(''), 3000);
        },
        error: (err) => {
          this.errorMessage.set('Erreur de création');
          console.error(err);
        }
      });
    }
  }

  deleteProfessionnel(id: number) {
    if (!confirm('Confirmer la suppression ?')) return;
    
    this.http.delete(`${this.apiUrl}/professionnels/manage/${id}/`, {
      withCredentials: true
    }).subscribe({
      next: () => {
        this.successMessage.set('Professionnel supprimé');
        this.loadProfessionnels();
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        this.errorMessage.set('Erreur de suppression');
        console.error(err);
      }
    });
  }

  deleteRendezVous(id: number) {
    if (!confirm('Confirmer la suppression du rendez-vous ?')) return;
    
    this.http.delete(`${this.apiUrl}/admin/rendez-vous/${id}/`, {
      withCredentials: true
    }).subscribe({
      next: () => {
        this.successMessage.set('Rendez-vous supprimé');
        this.loadRendezVous();
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        this.errorMessage.set('Erreur de suppression');
        console.error(err);
      }
    });
  }

  deleteClient(id: number) {
    if (!confirm('Confirmer la suppression du client ?')) return;
    
    this.http.delete(`${this.apiUrl}/admin/clients/${id}/`, {
      withCredentials: true
    }).subscribe({
      next: () => {
        this.successMessage.set('Client supprimé');
        this.loadClients();
        setTimeout(() => this.successMessage.set(''), 3000);
      },
      error: (err) => {
        this.errorMessage.set('Erreur de suppression');
        console.error(err);
      }
    });
  }

  cancel() {
    this.isEditingProf.set(false);
  }

  // Pagination
  getProfessionnelsPagines(): Professionnel[] {
    const debut = (this.pageProfessionnels() - 1) * this.parPage;
    return this.professionnels().slice(debut, debut + this.parPage);
  }

  getRendezVousPagines(): RendezVous[] {
    const debut = (this.pageRendezVous() - 1) * this.parPage;
    return this.rendezVous().slice(debut, debut + this.parPage);
  }

  getClientsPagines(): Client[] {
    const debut = (this.pageClients() - 1) * this.parPage;
    return this.clients().slice(debut, debut + this.parPage);
  }

  getTotalPagesProfessionnels(): number {
    return Math.ceil(this.professionnels().length / this.parPage);
  }

  getTotalPagesRendezVous(): number {
    return Math.ceil(this.rendezVous().length / this.parPage);
  }

  getTotalPagesClients(): number {
    return Math.ceil(this.clients().length / this.parPage);
  }

  nextPageProfessionnels() {
    if (this.pageProfessionnels() < this.getTotalPagesProfessionnels()) {
      this.pageProfessionnels.set(this.pageProfessionnels() + 1);
    }
  }

  prevPageProfessionnels() {
    if (this.pageProfessionnels() > 1) {
      this.pageProfessionnels.set(this.pageProfessionnels() - 1);
    }
  }

  nextPageRendezVous() {
    if (this.pageRendezVous() < this.getTotalPagesRendezVous()) {
      this.pageRendezVous.set(this.pageRendezVous() + 1);
    }
  }

  prevPageRendezVous() {
    if (this.pageRendezVous() > 1) {
      this.pageRendezVous.set(this.pageRendezVous() - 1);
    }
  }

  nextPageClients() {
    if (this.pageClients() < this.getTotalPagesClients()) {
      this.pageClients.set(this.pageClients() + 1);
    }
  }

  prevPageClients() {
    if (this.pageClients() > 1) {
      this.pageClients.set(this.pageClients() - 1);
    }
  }
}
