import { Component, OnInit } from '@angular/core';
import {UserService} from '../../services/user.service';
import {User} from '../../models/user.model';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  firstName = '';
  lastName = '';
  username = '';
  password = '';
  gender = '';

  currentFirstName: string | undefined = '';
  currentLastName: string | undefined = '';
  currentUsername: string | undefined = '';
  currentGender: string | undefined = '';

  constructor(private userService: UserService, private route: ActivatedRoute,
              private router: Router) { }

  ngOnInit(): void {
    this.userService.getUser(localStorage.getItem('object-detection-current-user'))
      .subscribe(currentUser => {
        this.currentFirstName = currentUser.firstName;
        this.currentLastName = currentUser.lastName;
        this.currentUsername = currentUser.username;
        this.currentGender = currentUser.gender;
      })
  }

  public updateUser() {
    let newUser: User = {};
    if (this.firstName !== '') {
      newUser.firstName = this.firstName;
    }

    if (this.lastName !== '') {
      newUser.lastName = this.lastName;
    }

    if (this.username !== '') {
      newUser.username = this.username;
    }

    if (this.gender !== '') {
      newUser.gender = this.gender;
    }

    if (this.password !== '') {
      newUser.password = this.password;
    }

    this.userService.patchUser(newUser, localStorage.getItem('object-detection-current-user'))
      .subscribe(newUser => {
        if (this.username !== '') {
          localStorage.setItem('object-detection-current-user', this.username);
        }

        this.userService.getUser(localStorage.getItem('object-detection-current-user'))
          .subscribe(currentUser => {
            this.currentFirstName = currentUser.firstName;
            this.currentLastName = currentUser.lastName;
            this.currentUsername = currentUser.username;
            this.currentGender = currentUser.gender;
          })
      });
  }

  onChangeGender(event: any) {
    this.gender = event.value;
  }

}
