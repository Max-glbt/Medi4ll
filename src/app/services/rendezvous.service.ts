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
    // Récupération depuis l'API backend avec l'utilisateur connecté
    const user = localStorage.getItem('currentUser');
    
    if (!user) {
      // Si pas d'utilisateur connecté, retourner un tableau vide
      return new Observable(observer => {
        observer.next([]);
        observer.complete();
      });
    }

    // Appel à l'API backend pour récupérer les rendez-vous de l'utilisateur connecté
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });
    
    return this.http.get<RendezVous[]>(`${this.apiUrl}/rendez-vous/`, { 
      headers,
      withCredentials: true 
    });

    // Anciennes données simulées (commentées pour référence)
    /*
    return new Observable(observer => {
      setTimeout(() => {
        observer.next([
          {
            id: 1,
            professionnel: {
              id: 1,
              nom: 'Martin',
              prenom: 'Sophie',
              email: 'sophie.martin@email.com',
              specialite: {
                id: 1,
                nom: 'Médecine générale',
                description: '',
                icone: ''
              },
              bio: '',
              photo_url: '',
              tarif_consultation: '25.00',
              accepte_teleconsultation: false,
              statut_validation: 'VALIDE'
            },
            cabinet: {
              id: 1,
              nom: 'Cabinet Médical Centre-Ville',
              adresse: '15 rue de la République',
              ville: 'Paris',
              code_postal: '75001',
              telephone: '01 23 45 67 89',
              latitude: '48.8566',
              longitude: '2.3522'
            },
            motif_consultation: {
              id: 1,
              libelle: 'Consultation générale',
              duree_estimee: 30,
              tarif: '25.00'
            },
            date: '2026-01-27',
            heure_debut: '14:30',
            heure_fin: '15:00',
            statut: 'CONFIRME',
            mode: 'PRESENTIEL',
            notes_patient: '',
            rappel_envoye: false,
            date_creation: '2026-01-15T10:00:00Z'
          },
          {
            id: 2,
            professionnel: {
              id: 2,
              nom: 'Dupont',
              prenom: 'Jean',
              email: 'jean.dupont@email.com',
              specialite: {
                id: 2,
                nom: 'Dentiste',
                description: '',
                icone: ''
              },
              bio: '',
              photo_url: '',
              tarif_consultation: '50.00',
              accepte_teleconsultation: false,
              statut_validation: 'VALIDE'
            },
            cabinet: {
              id: 2,
              nom: 'Cabinet Dentaire',
              adresse: '8 avenue des Champs',
              ville: 'Paris',
              code_postal: '75008',
              telephone: '01 98 76 54 32',
              latitude: '48.8698',
              longitude: '2.3082'
            },
            motif_consultation: {
              id: 2,
              libelle: 'Détartrage',
              duree_estimee: 45,
              tarif: '50.00'
            },
            date: '2026-01-31',
            heure_debut: '10:00',
            heure_fin: '10:45',
            statut: 'CONFIRME',
            mode: 'PRESENTIEL',
            notes_patient: '',
            rappel_envoye: false,
            date_creation: '2026-01-18T14:30:00Z'
          }
        ]);
        observer.complete();
      }, 500);
    });
    */
  }
}
