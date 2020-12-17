import {Component, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {HttpClient} from '@angular/common/http';
import {UserService} from '../../services/user.service';
import {PictureService} from '../../services/picture.service';

@Component({
  selector: 'app-sendphoto',
  templateUrl: './sendphoto.component.html',
  styleUrls: ['./sendphoto.component.scss']
})
export class SendPhotoComponent implements OnInit {
  @ViewChild("canvas") canvas: { nativeElement: HTMLCanvasElement; } | undefined;

  photo: string | null = '';
  notLoaded: boolean = false;

  constructor(private pictureService: PictureService, private route: ActivatedRoute,
              private router: Router) { }

  ngOnInit(): void {
    this.photo = localStorage.getItem('object-detection-takenphoto');
    localStorage.removeItem('object-detection-takenphoto');
  }

  private cx: CanvasRenderingContext2D | undefined;

  public ngAfterViewInit() {
    let canvasEl: HTMLCanvasElement;
    if (this.canvas !== undefined) {
      canvasEl = this.canvas.nativeElement;
    }
    else {
      alert('Error while getting canvas');
      return;
    }

    this.cx = canvasEl.getContext('2d')!;
    let image = new Image();

    canvasEl.width = 640;
    canvasEl.height = 480;

    this.cx.lineWidth = 3;
    this.cx.lineCap = 'round';
    this.cx.strokeStyle = '#000';
    image.onload = ()=> {
      if (this.cx !== undefined) {
        this.cx.save();
        this.cx.scale(-1,1);
        this.cx.drawImage(image,0,0,640*-1,480);
        this.cx.restore();
      }
      else {
        alert('Error while drawing canvas');
        return;
      }
    }
    if (this.photo != null) {
      image.src = this.photo;
    }
    else {
      alert('Error while getting image');
    }
  }

  sendToProcess() {
    this.notLoaded = !this.notLoaded;
    this.pictureService.sendPicture({'value': this.photo})
      .subscribe(id => {
        localStorage.setItem('object-detection-id-process', id.id.toString());
        this.router.navigate(['/result']);
      },
        error => {
          alert(error.status + ': ' + error.error);
        });
  }
}
