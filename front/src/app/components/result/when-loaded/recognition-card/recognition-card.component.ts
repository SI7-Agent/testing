import {Component, Input, OnInit} from '@angular/core';
import {ImageDetection} from '../../../../models/image-detection.model';

@Component({
  selector: 'app-recognition-card',
  templateUrl: './recognition-card.component.html',
  styleUrls: ['./recognition-card.component.scss']
})
export class RecognitionCardComponent implements OnInit {
  @Input() miniImg: ImageDetection | undefined;

  object: string | undefined = '';
  emote: string | undefined = '';
  gender: string | undefined = '';
  atPhoto: string | undefined = '';

  constructor() { }

  ngOnInit(): void {
    this.object = this.miniImg && this.miniImg.type;
    this.emote = this.miniImg && this.miniImg.emote;
    this.gender = this.miniImg && this.miniImg.gender;
    this.atPhoto = this.miniImg && this.miniImg.location;
  }

}
