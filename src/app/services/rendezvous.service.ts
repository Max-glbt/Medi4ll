import { Injectable, inject, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface RendezVous {
  id: number;
  professionnel: {
    id: number;
    nom: string;
    prenom: string;
    email: string;
    specialite: {
      id: number;
      nom: string;
      description: string;
      icone: string;
    };
    bio: string;
    photo_url: string;
    tarif_consultation: string;
    accepte_teleconsultation: boolean;
    statut_validation: string;
  };
  cabinet: {
    id: number;
    nom: string;
    adresse: string;
    ville: string;
    code_postal: string;
    telephone: string;
    latitude: string;
    longitude: string;
  };
  motif_consultation: {
    id: number;
    libelle: string;
    duree_estimee: number;
    tarif: string;
  } | null;
  date: string;
  heure_debut: string;
  heure_fin: string;
  statut: string;
  mode: string;
  notes_patient: string;
  rappel_envoye: boolean;
  date_creation: string;
}

@Injectable({
  providedIn: 'root'
})
export class RendezvousService {
  private http = inject(HttpClient);
  private apiUrl = '/api';

  getRendezVous(): Observable<RendezVous[]> {
    const user = localStorage.getItem('currentUser');
    
    if (!user) {
      return new Observable(observer => {
        observer.next([]);
        observer.complete();
      });
    }

    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
    return this.http.get<RendezVous[]>(`${this.apiUrl}/rendez-vous/`, { 
      headers,
      withCredentials: true 
    });
  }
}
