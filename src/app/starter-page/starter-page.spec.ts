import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StarterPage } from './starter-page';

describe('StarterPage', () => {
  let component: StarterPage;
  let fixture: ComponentFixture<StarterPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StarterPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StarterPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
