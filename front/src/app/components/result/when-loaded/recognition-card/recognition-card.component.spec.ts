import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecognitionCardComponent } from './recognition-card.component';

describe('RecognitionCardComponent', () => {
  let component: RecognitionCardComponent;
  let fixture: ComponentFixture<RecognitionCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RecognitionCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RecognitionCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
