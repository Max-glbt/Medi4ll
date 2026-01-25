import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Navbar } from "../navbar/navbar";
import { AuthService } from '../services/auth.service';


@Component({
  selector: 'app-home',
  imports: [Navbar, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  userDisplayName: string;
  motsCles = signal<string>('');

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
