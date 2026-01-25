import { Component, OnInit, AfterViewInit, inject, signal, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Navbar } from '../navbar/navbar';

declare var L: any;

interface Professionnel {
  id: number;
  nom: string;
  prenom: string;
  email: string;
  specialite: {
    id: number;
    nom: string;
    description: string;
  };
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

@Component({
  selector: 'app-detail-professionnel',
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './detail-professionnel.html',
  styleUrl: './detail-professionnel.css',
})
export class DetailProfessionnel implements OnInit, AfterViewInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private http = inject(HttpClient);

  professionnel = signal<Professionnel | null>(null);
  
  // Sélection de rendez-vous
  dateSelectionnee = signal<string>('');
  heureSelectionnee = signal<string>('');
  modeConsultation = signal<string>('PRESENTIEL');
  motif = signal<string>('');
  notes = signal<string>('');
  cabinetSelectionne = signal<number | null>(null);
  cabinetDetails = signal<{ id: number; nom: string; adresse: string; ville: string; code_postal: string; telephone: string } | null>(null);
  
  // États
  isLoading = signal<boolean>(false);
  errorMessage = signal<string>('');
  successMessage = signal<string>('');

  // Horaires disponibles (à adapter selon votre logique)
  horairesDispo = signal<string[]>([
    // Chargés depuis l'API en fonction de la date
  ]);

  // Carte
  private map: any = null;

  ngOnInit() {
    // Récupérer le professionnel depuis localStorage
    const professionnelJson = localStorage.getItem('professionnelSelectionne');
    if (professionnelJson) {
      const prof = JSON.parse(professionnelJson);
      this.professionnel.set(prof);
      this.modeConsultation.set(prof.accepte_teleconsultation ? 'PRESENTIEL' : 'PRESENTIEL');
      // Définir le cabinet par défaut (premier)
      const firstCab = prof.cabinets && prof.cabinets.length ? prof.cabinets[0] : null;
      if (firstCab) {
        this.cabinetSelectionne.set(firstCab.id);
        this.cabinetDetails.set(firstCab);
      }
    } else {
      this.router.navigate(['/prise-rdv']);
    }

    // Définir la date minimale à aujourd'hui
    const today = new Date().toISOString().split('T')[0];
    this.dateSelectionnee.set(today);
    this.fetchHorairesDisponibles(today);
  }

  ngAfterViewInit() {
    // Initialiser la carte après un délai pour s'assurer que le DOM est chargé
    setTimeout(() => this.initMap(), 100);
  }

  initMap() {
    const prof = this.professionnel();
    if (!prof || !prof.cabinets || prof.cabinets.length === 0) return;

    // Utiliser le cabinet sélectionné
    const selectedId = this.cabinetSelectionne();
    const cabinet = prof.cabinets.find(c => c.id === selectedId) || prof.cabinets[0];
    // Coordonnées par défaut (Paris centre) si géocodage échoue
    const defaultLat = 48.8566;
    const defaultLng = 2.3522;

    // Géocoder l'adresse du cabinet
    this.geocodeAddress(`${cabinet.adresse}, ${cabinet.code_postal} ${cabinet.ville}`, (lat: number, lng: number) => {
      // Détruire la carte existante si elle existe
      if (this.map) {
        this.map.remove();
      }

      // Créer la carte
      this.map = L.map('map').setView([lat, lng], 15);

      // Ajouter les tuiles OpenStreetMap
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
      }).addTo(this.map);

      // Ajouter un marqueur
      L.marker([lat, lng])
        .addTo(this.map)
        .bindPopup(`<b>${cabinet.nom}</b><br>${cabinet.adresse}<br>${cabinet.code_postal} ${cabinet.ville}`)
        .openPopup();
    });
  }

  geocodeAddress(address: string, callback: (lat: number, lng: number) => void) {
    // Utiliser Nominatim (service de géocodage OpenStreetMap gratuit)
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;
    
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data && data.length > 0) {
          const lat = parseFloat(data[0].lat);
          const lng = parseFloat(data[0].lon);
          callback(lat, lng);
        } else {
          // Utiliser Paris comme coordonnées par défaut
          callback(48.8566, 2.3522);
        }
      })
      .catch(error => {
        console.error('Erreur de géocodage:', error);
        callback(48.8566, 2.3522);
      });
  }

  onDateChange(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.dateSelectionnee.set(value);
    this.fetchHorairesDisponibles(value);
  }

  onHeureChange(event: Event) {
    const value = (event.target as HTMLSelectElement).value;
    this.heureSelectionnee.set(value);
  }

  onModeChange(event: Event) {
    const value = (event.target as HTMLSelectElement).value;
    this.modeConsultation.set(value);
  }

  onCabinetChange(event: Event) {
    const value = parseInt((event.target as HTMLSelectElement).value, 10);
    this.cabinetSelectionne.set(value);
    // Mettre à jour les détails du cabinet sélectionné
    const prof = this.professionnel();
    const selected = prof?.cabinets?.find(c => c.id === value) || null;
    if (selected) {
      this.cabinetDetails.set(selected);
    }
    // Recharger la carte et les disponibilités
    this.initMap();
    const date = this.dateSelectionnee();
    if (date) {
      this.fetchHorairesDisponibles(date);
    }
  }

  onMotifChange(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.motif.set(value);
  }

  onNotesChange(event: Event) {
    const value = (event.target as HTMLTextAreaElement).value;
    this.notes.set(value);
  }

  async confirmerRendezVous() {
    if (!this.dateSelectionnee() || !this.heureSelectionnee()) {
      this.errorMessage.set('Veuillez sélectionner une date et une heure');
      return;
    }

    this.isLoading.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    try {
      const prof = this.professionnel();
      const cabinetId = this.cabinetSelectionne();
      const cabinet = prof?.cabinets?.find(c => c.id === cabinetId);

      const rdvData = {
        professionnel_id: prof?.id,
        cabinet_id: cabinet?.id,
        date: this.dateSelectionnee(),
        heure_debut: this.heureSelectionnee(),
        mode: this.modeConsultation(),
        notes_patient: this.notes()
      };

      // Appel API pour créer le rendez-vous
      await this.http.post('/api/rendez-vous/create/', rdvData, {
        withCredentials: true
      }).toPromise();

      this.successMessage.set('Rendez-vous confirmé avec succès !');
      // Supprimer le créneau choisi de la liste des dispos immédiatement
      const selected = this.heureSelectionnee();
      this.horairesDispo.set(this.horairesDispo().filter(h => h !== selected));
      
      // Rediriger vers la page des rendez-vous après 2 secondes
      setTimeout(() => {
        this.router.navigate(['/reservation']);
      }, 2000);

    } catch (error: any) {
      console.error('Erreur lors de la création du rendez-vous:', error);
      const serverMsg = error.error?.error || error.error?.message;
      this.errorMessage.set(serverMsg || 'Erreur lors de la création du rendez-vous');
    } finally {
      this.isLoading.set(false);
    }
  }

  fetchHorairesDisponibles(date: string) {
    const prof = this.professionnel();
    if (!prof) return;
    this.isLoading.set(true);
    const cabinetId = this.cabinetSelectionne();
    const query = cabinetId ? `?date=${date}&cabinet_id=${cabinetId}` : `?date=${date}`;
    this.http.get<{ slots: string[] }>(`/api/professionnels/${prof.id}/disponibilites/${query}`, {
      withCredentials: false
    }).subscribe({
      next: (data) => {
        this.horairesDispo.set(data.slots || []);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Erreur chargement disponibilités:', err);
        this.horairesDispo.set([]);
        this.isLoading.set(false);
      }
    });
  }

  retour() {
    this.router.navigate(['/prise-rdv']);
  }
}
