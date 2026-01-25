import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { Navbar } from '../navbar/navbar';
import { RendezvousService, RendezVous } from '../services/rendezvous.service';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-reservation',
  imports: [CommonModule, Navbar, RouterModule],
  templateUrl: './reservation.html',
  styleUrl: './reservation.css',
})
export class Reservation implements OnInit {
  private rendezvousService = inject(RendezvousService);
  private authService = inject(AuthService);
  private router = inject(Router);
  
  rendezVousList = signal<RendezVous[]>([]);
  isLoading = signal(true);
  errorMessage = signal('');
  isAuthenticated = this.authService.isAuthenticated;

  // Pagination
  pageActuelle = signal<number>(1);
  parPage = 20;

  // Calendrier
  currentDate = signal(new Date());
  calendarDays = signal<any[]>([]);
  daysOfWeek = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];

  ngOnInit() {
    // Vérifier si l'utilisateur est connecté
    if (!this.authService.isAuthenticated()) {
      this.errorMessage.set('Vous devez être connecté pour voir vos rendez-vous.');
      this.isLoading.set(false);
      return;
    }
    this.loadRendezVous();
    this.generateCalendar();
  }

  loadRendezVous() {
    this.isLoading.set(true);
    this.errorMessage.set('');
    this.rendezvousService.getRendezVous().subscribe({
      next: (data) => {
        this.rendezVousList.set(data);
        this.isLoading.set(false);
        this.generateCalendar(); // Regénérer le calendrier avec les rendez-vous
      },
      error: (error) => {
        console.error('Erreur lors du chargement des rendez-vous:', error);
        if (error.status === 403 || error.status === 401) {
          this.errorMessage.set('Session expirée. Veuillez vous reconnecter.');
        } else if (error.status === 0) {
          this.errorMessage.set('Impossible de contacter le serveur. Vérifiez que le backend est démarré.');
        } else {
          this.errorMessage.set('Erreur de connexion à l\'API. Veuillez réessayer.');
        }
        this.isLoading.set(false);
      }
    });
  }

  generateCalendar() {
    const date = this.currentDate();
    const year = date.getFullYear();
    const month = date.getMonth();
    
    // Premier jour du mois
    const firstDay = new Date(year, month, 1);
    // Dernier jour du mois
    const lastDay = new Date(year, month + 1, 0);
    
    // Jour de la semaine du premier jour (0 = dimanche, 1 = lundi, etc.)
    let firstDayOfWeek = firstDay.getDay();
    // Convertir pour que lundi = 0
    firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;
    
    const daysInMonth = lastDay.getDate();
    const days: any[] = [];
    
    // Jours vides au début
    for (let i = 0; i < firstDayOfWeek; i++) {
      days.push({ day: null, isEmpty: true });
    }
    
    // Jours du mois
    const today = new Date();
    const rendezVousDates = this.getRendezVousDates();
    
    for (let day = 1; day <= daysInMonth; day++) {
      const currentDay = new Date(year, month, day);
      const dateStr = this.formatDateToYYYYMMDD(currentDay);
      
      days.push({
        day,
        isEmpty: false,
        isToday: this.isSameDay(currentDay, today),
        hasAppointment: rendezVousDates.includes(dateStr)
      });
    }
    
    this.calendarDays.set(days);
  }

  getRendezVousDates(): string[] {
    return this.rendezVousList().map(rdv => rdv.date);
  }

  formatDateToYYYYMMDD(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  isSameDay(date1: Date, date2: Date): boolean {
    return date1.getFullYear() === date2.getFullYear() &&
           date1.getMonth() === date2.getMonth() &&
           date1.getDate() === date2.getDate();
  }

  previousMonth() {
    const current = this.currentDate();
    this.currentDate.set(new Date(current.getFullYear(), current.getMonth() - 1, 1));
    this.generateCalendar();
  }

  nextMonth() {
    const current = this.currentDate();
    this.currentDate.set(new Date(current.getFullYear(), current.getMonth() + 1, 1));
    this.generateCalendar();
  }

  getMonthYear(): string {
    const date = this.currentDate();
    const months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];
    return `${months[date.getMonth()]} ${date.getFullYear()}`;
  }

  formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    const days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
    const months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 
                    'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'];
    return `${days[date.getDay()]} ${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
  }

  getStatutLabel(statut: string): string {
    const statuts: { [key: string]: string } = {
      'CONFIRME': 'Confirmé',
      'EN_ATTENTE': 'En attente',
      'ANNULE': 'Annulé',
      'TERMINE': 'Terminé'
    };
    return statuts[statut] || statut;
  }

  getModeLabel(mode: string): string {
    const modes: { [key: string]: string } = {
      'PRESENTIEL': 'Présentiel',
      'TELECONSULTATION': 'Téléconsultation'
    };
    return modes[mode] || mode;
  }

  // Pagination
  getRendezVousPagines(): RendezVous[] {
    const debut = (this.pageActuelle() - 1) * this.parPage;
    const fin = debut + this.parPage;
    return this.rendezVousList().slice(debut, fin);
  }

  getTotalPages(): number {
    return Math.ceil(this.rendezVousList().length / this.parPage);
  }

  pagePrecedente() {
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

  scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

