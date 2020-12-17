import { TestBed } from '@angular/core/testing';

import { PictureserviceService } from './picture.service';

describe('PictureserviceService', () => {
  let service: PictureserviceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PictureserviceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
