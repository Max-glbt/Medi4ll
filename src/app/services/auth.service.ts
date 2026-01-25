import { Injectable, signal, inject } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

export interface User {
  id?: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  token?: string;
  is_admin?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private apiUrl = '/api';
  
  private currentUserSignal = signal<User | null>(null);
  private isAuthenticatedSignal = signal<boolean>(false);

  currentUser = this.currentUserSignal.asReadonly();
  isAuthenticated = this.isAuthenticatedSignal.asReadonly();

  constructor() {
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
    
    if (user.first_name) {
      return user.first_name;
    }
    return user.username;
  }

  async register(userData: { firstName: string, lastName: string, email: string, password: string, accountType: 'client' | 'professionnel', specialite?: number | null }): Promise<any> {
    try {
      const payload = {
        username: userData.email.split('@')[0], // Utiliser la partie avant @ comme username
        first_name: userData.firstName,
        last_name: userData.lastName,
        email: userData.email,
        password: userData.password,
        type_compte: userData.accountType,
        specialite_id: userData.specialite
      };
      
      const response = await firstValueFrom(
        this.http.post(`${this.apiUrl}/register/`, payload, {
          withCredentials: true
        })
      );
      return response;
    } catch (error) {
      throw error;
    }
  }

  async loginWithCredentials(username: string, password: string): Promise<User> {
    try {
      const response: any = await firstValueFrom(
        this.http.post(`${this.apiUrl}/login/`, { username, password }, {
          withCredentials: true
        })
      );
      
      const user: User = {
        id: response.user.id,
        username: response.user.username,
        email: response.user.email,
        first_name: response.user.first_name,
        last_name: response.user.last_name,
        is_admin: response.user.is_admin || false
      };
      
      this.login(user);
      return user;
    } catch (error) {
      throw error;
    }
  }

  async loginWithEmail(email: string, password: string): Promise<User> {
    try {
      const response: any = await firstValueFrom(
        this.http.post(`${this.apiUrl}/login/`, { email, password }, {
          withCredentials: true
        })
      );
      const user: User = {
        id: response.user.id,
        username: response.user.username,
        email: response.user.email,
        first_name: response.user.first_name,
        last_name: response.user.last_name,
        is_admin: response.user.is_admin || false
      };
      this.login(user);
      return user;
    } catch (error) {
      throw error;
    }
  }

  isAdmin(): boolean {
    const user = this.currentUserSignal();
    return user?.is_admin || false;
  }
}
