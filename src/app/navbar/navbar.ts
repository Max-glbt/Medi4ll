import { Component, signal, computed } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, RouterLinkActive, CommonModule, FormsModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  showContactModal = signal(false);
  contactForm = signal({
    email: '',
    subject: '',
    message: ''
  });
  successMessage = signal('');
  errorMessage = signal('');
  isSending = signal(false);

  // Signal computed pour réagir aux changements de l'utilisateur
  isAdminComputed = computed(() => {
    const user = this.authService.currentUser();
    return user?.is_admin || false;
  });

  constructor(private authService: AuthService, private http: HttpClient) {
    const user = this.authService.currentUser();
    if (user) {
      this.contactForm.set({
        email: user.email,
        subject: '',
        message: ''
      });
    }
  }

  onLogout(): void {
    this.authService.logout();
  }

  isAdmin(): boolean {
    return this.isAdminComputed();
  }

  openContactModal(event: Event): void {
    event.preventDefault();
    const user = this.authService.currentUser();
    if (user) {
      this.contactForm.set({
        email: user.email,
        subject: '',
        message: ''
      });
    }
    this.showContactModal.set(true);
  }

  closeContactModal(): void {
    this.showContactModal.set(false);
    this.successMessage.set('');
    this.errorMessage.set('');
  }

  sendContactMessage(): void {
    const form = this.contactForm();
    
    if (!form.subject || !form.message) {
      this.errorMessage.set('Veuillez remplir tous les champs');
      return;
    }

    this.isSending.set(true);
    this.errorMessage.set('');

    // Simuler l'envoi d'email (vous pouvez créer un endpoint backend si besoin)
    setTimeout(() => {
      this.successMessage.set('Message envoyé avec succès à support@medi4all.fr');
      this.isSending.set(false);
      setTimeout(() => {
        this.closeContactModal();
      }, 2000);
    }, 1000);
  }
}
