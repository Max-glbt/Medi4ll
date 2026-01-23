import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';

export interface User {
  id?: number;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  token?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSignal = signal<User | null>(null);
  private isAuthenticatedSignal = signal<boolean>(false);

  currentUser = this.currentUserSignal.asReadonly();
  isAuthenticated = this.isAuthenticatedSignal.asReadonly();

  constructor(private router: Router) {
    this.loadUserFromStorage();
  }

  private loadUserFromStorage(): void {
    const userJson = localStorage.getItem('currentUser');
    if (userJson) {
      const user = JSON.parse(userJson);
      this.currentUserSignal.set(user);
      this.isAuthenticatedSignal.set(true);
    }
  }

  login(user: User): void {
    this.currentUserSignal.set(user);
    this.isAuthenticatedSignal.set(true);
    localStorage.setItem('currentUser', JSON.stringify(user));
  }

  logout(): void {
    this.currentUserSignal.set(null);
    this.isAuthenticatedSignal.set(false);
    localStorage.removeItem('currentUser');
    this.router.navigate(['/starter']);
  }

  getUserDisplayName(): string {
    const user = this.currentUserSignal();
    if (!user) return 'Utilisateur';
    
    if (user.firstName) {
      return user.firstName;
    }
    return user.username;
  }

  register(userData: any): Promise<any> {
    // TODO: Implémenter l'appel API
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve({ success: true, message: 'Inscription réussie' });
      }, 1000);
    });
  }

  loginWithCredentials(email: string, password: string): Promise<User> {
    // TODO: Implémenter l'appel API
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // Simulation de connexion
        const user: User = {
          id: 1,
          username: email.split('@')[0],
          email: email,
          firstName: 'Maxence',
          lastName: 'Test',
          token: 'fake-jwt-token'
        };
        resolve(user);
      }, 1000);
    });
  }
}
