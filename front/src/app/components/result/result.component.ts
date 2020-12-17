import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss']
})
export class ResultComponent implements OnInit {
  notLoaded: boolean = true;

  constructor() { }

  test_if(event: StorageEvent) {
    this.notLoaded = !this.notLoaded;
  }

  ngOnInit(): void {
    window.addEventListener('storage', this.test_if.bind(this));
  }

}
