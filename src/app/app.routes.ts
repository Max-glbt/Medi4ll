import { Routes } from '@angular/router';
import { StarterPage } from './starter-page/starter-page';
import { Home } from './home/home';
import { Reservation } from './reservation/reservation';
import { PriseRDVPage } from './prise-rdv-page/prise-rdv-page';
import { DetailProfessionnel } from './detail-professionnel/detail-professionnel';
import { ProfilPage } from './profil-page/profil-page';
import { AdminPage } from './admin-page/admin-page';
import { adminGuard } from './admin.guard';

export const routes: Routes = [
  { path: '', component: StarterPage },
  { path: 'starter', component: StarterPage },
  { path: 'home', component: Home },
  { path: 'reservation', component: Reservation },
  { path: 'prise-rdv', component: PriseRDVPage },
  { path: 'prise-rdv/:id', component: DetailProfessionnel },
  { path: 'profil', component: ProfilPage },
  { path: 'admin', component: AdminPage, canActivate: [adminGuard] },
];