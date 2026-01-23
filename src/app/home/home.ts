import { Component } from '@angular/core';
import { Navbar } from "../navbar/navbar";
import { AuthService } from '../services/auth.service';


@Component({
  selector: 'app-home',
  imports: [Navbar],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {
  userDisplayName: string;

  constructor(private authService: AuthService) {
    this.userDisplayName = this.authService.getUserDisplayName();
  }
}
