import { Routes } from '@angular/router';
import { StarterPage } from './starter-page/starter-page';
import { Home } from './home/home';
import { Reservation } from './reservation/reservation';
import { PriseRDVPage } from './prise-rdv-page/prise-rdv-page';

export const routes: Routes = [
  { path: '', component: StarterPage },
  { path: 'starter', component: StarterPage },
  { path: 'home', component: Home },
  { path: 'reservation', component: Reservation },
  { path: 'prise-rdv', component: PriseRDVPage },
];