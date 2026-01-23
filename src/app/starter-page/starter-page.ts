import { Component, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-starter-page',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './starter-page.html',
  styleUrl: './starter-page.css',
})
export class StarterPage {
  showMode: 'buttons' | 'login' | 'register' = 'buttons';
  loginForm: FormGroup;
  registerForm: FormGroup;
  errorMessage = '';
  successMessage = '';
  isLoading = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthService
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
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordMatchValidator });
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
    this.showMode = 'register';
    this.errorMessage = '';
    this.successMessage = '';
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

    // Appel du service d'authentification
    this.authService.loginWithCredentials(email, password)
      .then(user => {
        this.authService.login(user);
        this.isLoading = false;
        this.router.navigate(['/home']);
      })
      .catch(error => {
        this.isLoading = false;
        this.errorMessage = error.message || 'Erreur lors de la connexion';
      });
  }

  onRegister() {
    if (this.registerForm.invalid) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const { firstName, lastName, email, password } = this.registerForm.value;

    // Appel du service d'authentification
    this.authService.register({ firstName, lastName, email, password })
      .then(response => {
        this.isLoading = false;
        
        // Connexion automatique après inscription
        const user = {
          username: email.split('@')[0],
          email: email,
          firstName: firstName,
          lastName: lastName
        };
        this.authService.login(user);
        
        // Redirection vers la page d'accueil
        this.router.navigate(['/home']);
      })
      .catch(error => {
        this.isLoading = false;
        this.errorMessage = error.message || 'Erreur lors de l\'inscription';
      });
  }
}
