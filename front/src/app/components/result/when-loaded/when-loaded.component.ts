import { Component, OnInit } from '@angular/core';
import {Type} from '../../../models/type.model';
import {PictureService} from '../../../services/picture.service';
import {FilterElementComponent} from './filter-element/filter-element.component';
import {ImageDetection} from '../../../models/image-detection.model';

@Component({
  selector: 'app-when-loaded',
  templateUrl: './when-loaded.component.html',
  styleUrls: ['./when-loaded.component.scss']
})
export class WhenLoadedComponent implements OnInit {
  fullPhoto: string = ''
  smthFound: boolean = true;

  filterNames: {label: string, tag: string}[] = [];
  currentStates: {value: string, tag:string, status: boolean}[] = [];
  detections: ImageDetection[] = [];

  private emotions: string | undefined;
  private objects: string | undefined;
  private genders: string | undefined;

  constructor(private pictureService: PictureService) { }

  ngOnInit(): void {
    this.emotions = '';
    this.objects = '';
    this.genders = '';

    this.pictureService.getTypes()
      .subscribe(types => {
        types.forEach((item, i, types) => {
          this.filterNames.push({label: item.value, tag: item.tag});
          this.currentStates.push({value: item.value, tag: item.tag, status: false});
        });
      }, error => {
        alert(error.status + ': ' + error.error);
      });

    this.pictureService.getFullDetections(parseInt(<string> localStorage.getItem('object-detection-id-process')))
      .subscribe(photo => {
        this.fullPhoto = photo.value;

        this.pictureService.getDetections(parseInt(<string> localStorage.getItem('object-detection-id-process')),
          '', '', '')
          .subscribe(detections => {
            this.smthFound = true;
            this.detections = detections;
          }, error => {
            this.smthFound = false;
            alert(error.status + ': ' + error.error);
          });
      }, error => {
        alert('Error while getting picture');
      });
  }

  doSearch($event: {value: string; status: boolean}) {
    let i = 0;
    while (this.currentStates[i].value != $event.value) {
      i++;
    }
    this.currentStates[i].status = $event.status;

    this.currentStates.forEach((item, i, arr) => {
      if (item.status && item.tag === "object") {
        this.objects += item.value + ",";
      }

      if (item.status && item.tag === "emotion") {
        this.emotions += item.value + ",";
      }

      if (item.status && item.tag === "gender") {
        this.genders += item.value + ",";
      }
    });

    this.pictureService.getDetections(parseInt(<string> localStorage.getItem('object-detection-id-process')),
      this.objects, this.emotions, this.genders)
      .subscribe(detections => {
        this.smthFound = true;
        this.detections = detections;
      }, error => {
        this.smthFound = false;
        alert(error.status + ': ' + error.error);
      });

    this.emotions = '';
    this.objects = '';
    this.genders = '';
  }
}
