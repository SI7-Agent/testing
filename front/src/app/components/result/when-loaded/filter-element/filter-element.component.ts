import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
  selector: 'app-filter-element',
  templateUrl: './filter-element.component.html',
  styleUrls: ['./filter-element.component.scss']
})
export class FilterElementComponent implements OnInit {
  @Output() public updateFilters: EventEmitter<{ value: string, status: boolean}> = new EventEmitter<{value: string, status: boolean}>();
  @Input() name: string = '';
  @Input() tag: string = '';

  constructor() { }

  ngOnInit(): void {
  }

  onChange(event: any): void {
    let data = {
      value: this.name,
      // status: event.target.checked
      status: event.checked
    }
    this.updateFilters.emit(data);
  }
}
