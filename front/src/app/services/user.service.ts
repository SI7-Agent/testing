import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import { Observable } from 'rxjs';
import { Token } from '../models/token.model';
import {User} from '../models/user.model';

@Injectable()
export class UserService {
  private url = `${environment.baseUrl}users`;

  constructor(private http: HttpClient) { }

  getLoginToken(login: string, password: string): Observable<Token> {
    let paramsList = new HttpParams();
    paramsList = paramsList.append('username', login);
    paramsList = paramsList.append('password', password);
    return this.http.get<Token>(`${this.url + '/login'}`, {params: paramsList});
  }

  register(person: any){
    const myHeaders = new HttpHeaders({
      'Content-Type': 'application/json;charset=utf-8'
    });
    return this.http.post<User>(`${this.url}`, person, {headers: myHeaders});
  }

  patchUser(newUser: User, username: string | null) {
    const myHeaders = new HttpHeaders({
      'Content-Type': 'application/json;charset=utf-8',
      // @ts-ignore
      'Authorization': localStorage.getItem('object-detection-token')
    });
    return this.http.patch(`${this.url}/${username}`, newUser, {headers:myHeaders});
  }

  getUser(username: string | null) {
    const myHeaders = new HttpHeaders({
      'Content-Type': 'application/json;charset=utf-8',
      // @ts-ignore
      'Authorization': localStorage.getItem('object-detection-token')
    });
    return this.http.get<User>(`${this.url}/${username}`, {headers:myHeaders});
  }

  deleteUser(username: string) {
    const myHeaders = new HttpHeaders({
      'Content-Type': 'application/json;charset=utf-8',
      // @ts-ignore
      'Authorization': localStorage.getItem('object-detection-token')
    });
    return this.http.delete(`${this.url}/${username}`, {headers:myHeaders});
  }

  logOut() {
    localStorage.removeItem('object-detection-token');
    localStorage.removeItem('object-detection-id-process');
    localStorage.removeItem('object-detection-current-user');
  }

}
