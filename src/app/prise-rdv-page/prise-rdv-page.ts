import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';
import { Navbar } from '../navbar/navbar';

interface Specialite {
  id: number;
  nom: string;
  description: string;
  icone?: string;
}

interface Cabinet {
  id: number;
  nom: string;
  adresse: string;
  ville: string;
  code_postal: string;
  telephone: string;
}

interface Professionnel {
  id: number;
  nom: string;
  prenom: string;
  email: string;
  specialite: Specialite;
  bio?: string;
  photo_url?: string;
  tarif_consultation: string;
  accepte_teleconsultation: boolean;
  cabinets?: Cabinet[];
}

@Component({
  selector: 'app-prise-rdv-page',
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './prise-rdv-page.html',
  styleUrl: './prise-rdv-page.css',
})
export class PriseRDVPage implements OnInit {
  private http = inject(HttpClient);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  
  specialites = signal<Specialite[]>([]);
  professionnels = signal<Professionnel[]>([]);
  professionnelsFiltres = signal<Professionnel[]>([]);
  
  pageActuelle = signal<number>(1);
  parPage = 20;
  
  motsCles = signal<string>('');
  villeRecherche = signal<string>('');
  specialiteSelectionnee = signal<number | null>(null);
  prixMax = signal<number | null>(null);
  
  isLoading = signal<boolean>(false);
  errorMessage = signal<string>('');

  ngOnInit() {
    this.chargerDonnees();
    
    this.route.queryParams.subscribe(params => {
      if (params['q']) {
        this.motsCles.set(params['q']);
        setTimeout(() => this.rechercherProfessionnels(), 100);
      }
    });
  }

  async chargerDonnees() {
    this.isLoading.set(true);
    this.errorMessage.set('');
    
    try {
      const specialites = await this.http.get<Specialite[]>('/api/specialites/', {
        withCredentials: true
      }).toPromise();
      this.specialites.set(specialites || []);
      
      const professionnels = await this.http.get<Professionnel[]>('/api/professionnels/', {
        withCredentials: true
      }).toPromise();
      this.professionnels.set(professionnels || []);
      this.professionnelsFiltres.set(professionnels || []);
      
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
      this.errorMessage.set('Erreur lors du chargement des données');
    } finally {
      this.isLoading.set(false);
    }
  }

  rechercherProfessionnels() {
    const motsCles = this.motsCles().toLowerCase().trim();
    const ville = this.villeRecherche().toLowerCase().trim();
    const specialiteId = this.specialiteSelectionnee();
    const prixMax = this.prixMax();
    
    let resultats = this.professionnels();
    
    if (motsCles) {
      resultats = resultats.filter(prof => {
        const nomComplet = `${prof.nom} ${prof.prenom}`.toLowerCase();
        const specialite = prof.specialite.nom.toLowerCase();
        const villes = prof.cabinets?.map(c => c.ville.toLowerCase()).join(' ') || '';
        
        return nomComplet.includes(motsCles) ||
               specialite.includes(motsCles) ||
               villes.includes(motsCles);
      });
    }
    
    if (ville) {
      resultats = resultats.filter(prof => 
        prof.cabinets?.some(cabinet => 
          cabinet.ville.toLowerCase().includes(ville) ||
          cabinet.code_postal.includes(ville) ||
          cabinet.adresse.toLowerCase().includes(ville)
        )
      );
    }
    
    if (specialiteId) {
      resultats = resultats.filter(prof => prof.specialite.id === specialiteId);
    }
    
    if (prixMax !== null) {
      resultats = resultats.filter(prof => parseFloat(prof.tarif_consultation) <= prixMax);
    }
    
    this.professionnelsFiltres.set(resultats);
    this.pageActuelle.set(1);
  }

  reinitialiserFiltres() {
    this.motsCles.set('');
    this.villeRecherche.set('');
    this.specialiteSelectionnee.set(null);
    this.prixMax.set(null);
    this.professionnelsFiltres.set(this.professionnels());
    this.pageActuelle.set(1);
  }

  getProfessionnelsPagines(): Professionnel[] {
    const debut = (this.pageActuelle() - 1) * this.parPage;
    const fin = debut + this.parPage;
    return this.professionnelsFiltres().slice(debut, fin);
  }

  getTotalPages(): number {
    return Math.ceil(this.professionnelsFiltres().length / this.parPage);
  }

  pagesPrecedente() {
    if (this.pageActuelle() > 1) {
      this.pageActuelle.set(this.pageActuelle() - 1);
      this.scrollToTop();
    }
  }

  pageSuivante() {
    if (this.pageActuelle() < this.getTotalPages()) {
      this.pageActuelle.set(this.pageActuelle() + 1);
      this.scrollToTop();
    }
  }

  allerALaPage(page: number) {
    this.pageActuelle.set(page);
    this.scrollToTop();
  }

  scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  getPagesAffichees(): number[] {
    const total = this.getTotalPages();
    const current = this.pageActuelle();
    const pages: number[] = [];
    
    pages.push(1);
    
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
      pages.push(i);
    }
    
    if (total > 1) {
      pages.push(total);
    }
    
    return [...new Set(pages)].sort((a, b) => a - b);
  }

  onMotsClesChange(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.motsCles.set(value);
    this.rechercherProfessionnels();
  }

  onVilleChange(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.villeRecherche.set(value);
    this.rechercherProfessionnels();
  }

  onSpecialiteChange(event: Event) {
    const value = (event.target as HTMLSelectElement).value;
    this.specialiteSelectionnee.set(value ? parseInt(value) : null);
    this.rechercherProfessionnels();
  }

  onPrixMaxChange(event: Event) {
    const value = (event.target as HTMLInputElement).value;
    this.prixMax.set(value ? parseFloat(value) : null);
    this.rechercherProfessionnels();
  }

  getCabinetsString(professionnel: Professionnel): string {
    if (!professionnel.cabinets || professionnel.cabinets.length === 0) {
      return 'Cabinet non renseigné';
    }
    return professionnel.cabinets.map(c => `${c.nom} - ${c.ville}`).join(', ');
  }

  getPremierCabinet(professionnel: Professionnel): Cabinet | null {
    return professionnel.cabinets && professionnel.cabinets.length > 0 
      ? professionnel.cabinets[0] 
      : null;
  }

  ouvrirDetailsProfessionnel(professionnel: Professionnel) {
    localStorage.setItem('professionnelSelectionne', JSON.stringify(professionnel));
    this.router.navigate(['/prise-rdv', professionnel.id]);
  }
}
