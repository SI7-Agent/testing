import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoadBarComponent } from './load-bar.component';

describe('LoadBarComponent', () => {
  let component: LoadBarComponent;
  let fixture: ComponentFixture<LoadBarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LoadBarComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoadBarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
