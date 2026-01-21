import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PriseRDVPage } from './prise-rdv-page';

describe('PriseRDVPage', () => {
  let component: PriseRDVPage;
  let fixture: ComponentFixture<PriseRDVPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PriseRDVPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PriseRDVPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
