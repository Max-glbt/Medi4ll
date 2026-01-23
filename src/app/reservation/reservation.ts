import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Navbar } from '../navbar/navbar';

@Component({
  selector: 'app-reservation',
  imports: [CommonModule, Navbar],
  templateUrl: './reservation.html',
  styleUrl: './reservation.css',
})
export class Reservation {

}
