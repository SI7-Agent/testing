import { Component, OnInit } from '@angular/core';
import {Observable, Subject} from 'rxjs';
import {WebcamImage, WebcamInitError, WebcamUtil} from 'ngx-webcam';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-takephoto',
  templateUrl: './takephoto.component.html',
  styleUrls: ['./takephoto.component.scss']
})
export class TakePhotoComponent implements OnInit {
  public showWebcam = true;
  public multipleWebcamsAvailable = false;
  public videoOptions: MediaTrackConstraints = {
    // width: {ideal: 1024},
    // height: {ideal: 576}
  };
  public errors: WebcamInitError[] = [];

  public webcamImage: WebcamImage | undefined;
  private trigger: Subject<void> = new Subject<void>();

  constructor(private route: ActivatedRoute,
              private router: Router) { }

  public ngOnInit(): void {
    WebcamUtil.getAvailableVideoInputs()
      .then((mediaDevices: MediaDeviceInfo[]) => {
        this.multipleWebcamsAvailable = mediaDevices && mediaDevices.length > 1;
      });
  }

  public triggerSnapshot(): void {
    this.trigger.next();
  }

  public toggleWebcam(): void {
    this.showWebcam = !this.showWebcam;
  }

  public handleInitError(error: WebcamInitError): void {
    this.errors.push(error);
  }

  public handleImage(webcamImage: WebcamImage): void {
    localStorage.setItem('object-detection-takenphoto', webcamImage.imageAsDataUrl);
    // @ts-ignore
    this.webcamImage = WebcamImage;
  }

  public get triggerObservable(): Observable<void> {
    return this.trigger.asObservable();
  }

  public makePhoto() {
    this.triggerSnapshot();
    this.router.navigate(['/sendphoto']);
  }
}
