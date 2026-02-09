import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { Navbar } from '../navbar/navbar';
import { RendezvousService, RendezVous } from '../services/rendezvous.service';
import { AuthService } from '../services/auth.service';
import { ConstantsService } from '../services/constants.service';

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
  private constantsService = inject(ConstantsService);
  
  rendezVousList = signal<RendezVous[]>([]);
  isLoading = signal(true);
  errorMessage = signal('');
  isAuthenticated = this.authService.isAuthenticated;

  pageActuelle = signal<number>(1);
  parPage = 20;

  currentDate = signal(new Date());
  calendarDays = signal<any[]>([]);
  daysOfWeek = Array.from({ length: 7 }, (_, i) => 
    new Intl.DateTimeFormat('fr-FR', { weekday: 'short' }).format(new Date(2024, 0, 1 + i))
  );

  ngOnInit() {
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
        this.generateCalendar(); 
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
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    
    let firstDayOfWeek = firstDay.getDay();
    firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;
    
    const daysInMonth = lastDay.getDate();
    const days: any[] = [];
    
    for (let i = 0; i < firstDayOfWeek; i++) {
      days.push({ day: null, isEmpty: true });
    }
    
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
    return new Intl.DateTimeFormat('fr-FR', { 
      month: 'long', 
      year: 'numeric' 
    }).format(date);
  }

  formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('fr-FR', { 
      weekday: 'long', 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric' 
    }).format(date);
  }

  getStatutLabel(statut: string): string {
    return this.constantsService.getStatutLabel(statut);
  }

  getModeLabel(mode: string): string {
    return this.constantsService.getModeLabel(mode);
  }

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

