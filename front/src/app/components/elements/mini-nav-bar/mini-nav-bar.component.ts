import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from '../../../services/user.service';

@Component({
  selector: 'app-mini-nav-bar',
  templateUrl: './mini-nav-bar.component.html',
  styleUrls: ['./mini-nav-bar.component.scss']
})
export class MiniNavBarComponent implements OnInit {

  constructor(private userService: UserService, private route: ActivatedRoute,
              private router: Router) { }

  ngOnInit(): void {
  }

  logout() {
    this.userService.logOut();
    this.router.navigate(['/login']);
  }
}
