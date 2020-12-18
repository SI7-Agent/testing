import { Component, OnInit } from '@angular/core';
import {UserService} from '../../services/user.service';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {
  login: string = '';
  password: string = '';
  firstName: string = '';
  lastName: string = '';
  gender: string = '';

  constructor(private userService: UserService, private route: ActivatedRoute,
              private router: Router) { }

  ngOnInit(): void {
  }

  async register() {
    if (this.login !== '' &&
      this.password !== '' &&
      this.firstName !== '' &&
      this.lastName !== '' &&
      this.gender !== '') {
      let newPerson = {
        "username": this.login,
        "firstName": this.firstName,
        "lastName": this.lastName,
        "password": this.password,
        "gender": this.gender
      };

      await this.userService.register(newPerson)
        .subscribe(new_user => {
          this.userService.getLoginToken(newPerson.username, newPerson.password)
            .subscribe(token => {
                localStorage.setItem('object-detection-token', <string> token['token']);
                localStorage.setItem('object-detection-current-user', newPerson.username);
                this.router.navigate(['/main']);
              },
              error => {
                alert(error.status + ': ' + error.error);
              });
      },
          error => {
            alert(error.status + ': ' + error.error);
      });
    }
    else {
        alert('Some fields are empty');
    }
  }

  onChangeGender(event: any) {
    this.gender = event.value;
  }
}
