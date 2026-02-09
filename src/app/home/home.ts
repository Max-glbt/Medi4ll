import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Navbar } from "../navbar/navbar";
import { AuthService } from '../services/auth.service';


@Component({
  selector: 'app-home',
  imports: [Navbar, FormsModule, CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  userDisplayName: string;
  motsCles = signal<string>('');
  
  stats = [
    { icon: '🩺', value: '2000+', label: 'Professionnels de santé' },
    { icon: '📋', value: '50k+', label: 'Rendez-vous réservés' },
    { icon: '💯', value: '4.8/5', label: 'Satisfaction patients' },
    { icon: '🏢', value: '500+', label: 'Cabinets partenaires' }
  ];

  articles: { title: string; excerpt: string; category: string; readTime: string; date: string; icon: string; }[] = [
    {
      title: 'Prévenir les maladies cardiovasculaires',
      excerpt: 'Adoptez des habitudes simples pour protéger votre cœur au quotidien : alimentation équilibrée, activité physique, gestion du stress et suivi médical.',
      category: 'Prévention',
      readTime: '4 min',
      date: '2026-02-01',
      icon: '❤️'
    },
    {
      title: 'Sommeil: améliorer la qualité en 5 étapes',
      excerpt: 'Routine régulière, environnement propice, réduction des écrans, hydratation maîtrisée et consultation en cas d’insomnie persistante.',
      category: 'Bien-être',
      readTime: '3 min',
      date: '2026-01-25',
      icon: '😴'
    },
    {
      title: 'Vaccinations: calendrier et rappels utiles',
      excerpt: 'Comprendre les rappels recommandés selon l’âge et les situations particulières pour rester protégé efficacement.',
      category: 'Santé publique',
      readTime: '5 min',
      date: '2026-01-12',
      icon: '💉'
    }
  ];

  constructor(
    private authService: AuthService,
    private router: Router
  ) {
    this.userDisplayName = this.authService.getUserDisplayName();
  }

  rechercher() {
    const recherche = this.motsCles().trim();
    if (recherche) {
      this.router.navigate(['/prise-rdv'], {
        queryParams: { q: recherche }
      });
    } else {
      this.router.navigate(['/prise-rdv']);
    }
  }
}
