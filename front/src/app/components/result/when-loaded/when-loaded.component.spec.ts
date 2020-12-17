import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WhenLoadedComponent } from './when-loaded.component';

describe('WhenLoadedComponent', () => {
  let component: WhenLoadedComponent;
  let fixture: ComponentFixture<WhenLoadedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WhenLoadedComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WhenLoadedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
