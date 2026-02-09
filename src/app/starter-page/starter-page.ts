import { Component, signal, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../services/auth.service';

interface Specialite {
  id: number;
  nom: string;
}

@Component({
  selector: 'app-starter-page',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './starter-page.html',
  styleUrl: './starter-page.css',
})
export class StarterPage implements OnInit {
  showMode: 'buttons' | 'login' | 'register' | 'register-type' = 'buttons';
  accountType: 'client' | 'professionnel' = 'client';
  loginForm: FormGroup;
  registerForm: FormGroup;
  errorMessage = '';
  successMessage = '';
  isLoading = false;
  specialites = signal<Specialite[]>([]);
  private apiUrl = '/api';

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService,
    private http: HttpClient
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });

    this.registerForm = this.fb.group({
      firstName: ['', [Validators.required]],
      lastName: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]],
      specialite: ['']
    }, { validators: this.passwordMatchValidator });
  }

  ngOnInit() {
    this.loadSpecialites();
  }

  loadSpecialites() {
    this.http.get<Specialite[]>(`${this.apiUrl}/specialites/`).subscribe({
      next: (data) => this.specialites.set(data),
      error: (err) => console.error('Erreur chargement spécialités:', err)
    });
  }

  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const confirmPassword = form.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { passwordMismatch: true };
  }

  showLogin() {
    this.showMode = 'login';
    this.errorMessage = '';
    this.successMessage = '';
  }

  showRegister() {
    this.showMode = 'register-type';
    this.errorMessage = '';
    this.successMessage = '';
  }

  selectAccountType(type: 'client' | 'professionnel') {
    this.accountType = type;
    this.showMode = 'register';
    this.errorMessage = '';
    this.successMessage = '';
    
    if (type === 'professionnel') {
      this.registerForm.get('specialite')?.setValidators([Validators.required]);
    } else {
      this.registerForm.get('specialite')?.clearValidators();
    }
    this.registerForm.get('specialite')?.updateValueAndValidity();
  }

  showButtons() {
    this.showMode = 'buttons';
    this.errorMessage = '';
    this.successMessage = '';
    this.loginForm.reset();
    this.registerForm.reset();
  }

  onLogin() {
    if (this.loginForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';

    const { email, password } = this.loginForm.value;

    this.authService.loginWithEmail(email, password)
      .then(user => {
        this.authService.login(user);
        this.isLoading = false;
        this.router.navigate(['/home']);
      })
      .catch(error => {
        this.isLoading = false;
        this.errorMessage = error.error?.error || 'Identifiants incorrects. Vérifiez votre email et mot de passe.';
      });
  }

  onRegister() {
    if (this.registerForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const { firstName, lastName, email, password, specialite } = this.registerForm.value;

    this.authService.register({ 
      firstName, 
      lastName, 
      email, 
      password,
      accountType: this.accountType,
      specialite: this.accountType === 'professionnel' ? specialite : null
    })
      .then(async (response) => {
        this.isLoading = false;
        
        try {
          const user = await this.authService.loginWithEmail(email, password);
          this.authService.login(user);
          this.router.navigate(['/home']);
        } catch (e) {
          this.errorMessage = 'Compte créé, mais connexion automatique impossible. Veuillez vous connecter.';
        }
      })
      .catch(error => {
        this.isLoading = false;
        this.errorMessage = error.message || 'Erreur lors de l\'inscription';
      });
  }
}
