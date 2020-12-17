import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {Observable} from 'rxjs';
import {Picture} from '../models/picture.model';
import {User} from '../models/user.model';
import {Id} from '../models/id.modell';
import {Type} from '../models/type.model';
import {ImageDetection} from '../models/image-detection.model';

@Injectable({
  providedIn: 'root'
})
export class PictureService {
  private urlImage = `${environment.baseUrl}images`;
  private urlType = `${environment.baseUrl}types`;

  constructor(private http: HttpClient) { }

  sendPicture(picture: { value: string | null }) {
    const myHeaders = new HttpHeaders({
      'Content-Type': 'application/json;charset=utf-8',
      // @ts-ignore
      'Authorization': localStorage.getItem('object-detection-token')
    });
    return this.http.post<Id>(`${this.urlImage}`, picture, {headers: myHeaders});
  }

  getTypes(types?: string) {
    const myHeaders = new HttpHeaders({
      'Content-Type': 'application/json;charset=utf-8',
      // @ts-ignore
      'Authorization': localStorage.getItem('object-detection-token')
    });

    let paramsList = new HttpParams();
    if (types !== undefined) {
      paramsList = paramsList.append('filter', types);
    }
    return this.http.get<Type[]>(`${this.urlType}`, {headers: myHeaders, params: paramsList});
  }

  getDetections(id: number, type?: string, emotion?: string, gender?: string) {
    const myHeaders = new HttpHeaders({
      'Content-Type': 'application/json;charset=utf-8',
      // @ts-ignore
      'Authorization': localStorage.getItem('object-detection-token')
    });

    let paramsList = new HttpParams();
    if (type !== undefined && type !== '') {
      paramsList = paramsList.append('type', type);
    }

    if (emotion !== undefined && emotion !== '') {
      paramsList = paramsList.append('emotion', emotion);
    }

    if (gender !== undefined && gender !== '') {
      paramsList = paramsList.append('gender', gender);
    }
    return this.http.get<ImageDetection[]>(`${this.urlImage}/${id}/detections`, {headers: myHeaders, params: paramsList});
  }

  getFullDetections(id: number) {
    const myHeaders = new HttpHeaders({
      'Content-Type': 'application/json;charset=utf-8',
      // @ts-ignore
      'Authorization': localStorage.getItem('object-detection-token')
    });

    return this.http.get<Picture>(`${this.urlImage}/${id}`, {headers: myHeaders});
  }
}
