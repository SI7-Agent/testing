import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OneMoreComponentComponent } from './sendphoto.component';

describe('OneMoreComponentComponent', () => {
  let component: OneMoreComponentComponent;
  let fixture: ComponentFixture<OneMoreComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OneMoreComponentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OneMoreComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
