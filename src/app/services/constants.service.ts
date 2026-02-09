import { Injectable } from '@angular/core';

export const STATUTS_LABELS: Record<string, string> = {
  'EN_ATTENTE': 'En attente',
  'CONFIRME': 'Confirmé',
  'TERMINE': 'Terminé',
  'ANNULE': 'Annulé'
};

export const STATUTS_BADGE_CLASSES: Record<string, string> = {
  'EN_ATTENTE': 'badge-warning',
  'CONFIRME': 'badge-success',
  'TERMINE': 'badge-info',
  'ANNULE': 'badge-danger'
};

export const MODES_LABELS: Record<string, string> = {
  'PRESENTIEL': 'Présentiel',
  'TELECONSULTATION': 'Téléconsultation'
};

@Injectable({
  providedIn: 'root'
})
export class ConstantsService {
  getStatutLabel(statut: string): string {
    return STATUTS_LABELS[statut] || statut;
  }

  getStatutBadgeClass(statut: string): string {
    return STATUTS_BADGE_CLASSES[statut] || 'badge-default';
  }

  getModeLabel(mode: string): string {
    return MODES_LABELS[mode] || mode;
  }
}
