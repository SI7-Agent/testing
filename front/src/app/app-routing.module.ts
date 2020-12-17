import { NgModule } from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {TakePhotoComponent} from './components/takephoto/takephoto.component';
import {SendPhotoComponent} from './components/sendphoto/sendphoto.component';
import {LoginComponent} from './components/login/login.component';
import {RegistrationComponent} from './components/registration/registration.component';
import {ProfileComponent} from './components/profile/profile.component';
import {ResultComponent} from './components/result/result.component';
import {MainComponent} from './components/main/main.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegistrationComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'main', component: MainComponent },
  { path: 'takephoto', component: TakePhotoComponent },
  { path: 'sendphoto', component: SendPhotoComponent },
  { path: 'result', component: ResultComponent },
  { path: '**', redirectTo: 'main' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
