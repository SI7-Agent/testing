import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { TakePhotoComponent } from './components/takephoto/takephoto.component';
import { AppRoutingModule } from './app-routing.module';
import { WebcamModule } from 'ngx-webcam';
import { HttpClientModule } from '@angular/common/http';
import { SendPhotoComponent } from './components/sendphoto/sendphoto.component';
import { ProfileComponent } from './components/profile/profile.component';
import { LoginComponent } from './components/login/login.component';
import { RegistrationComponent } from './components/registration/registration.component';
import { ResultComponent } from './components/result/result.component';
import { MainComponent } from './components/main/main.component';
import { PictureService } from './services/picture.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { UserService } from './services/user.service';
import { MiniNavBarComponent } from './components/elements/mini-nav-bar/mini-nav-bar.component';
import { MatIconModule } from '@angular/material/icon';
import { LoadBarComponent } from './components/elements/load-bar/load-bar.component';
import { WhenLoadedComponent } from './components/result/when-loaded/when-loaded.component';
import { RecognitionCardComponent } from './components/result/when-loaded/recognition-card/recognition-card.component';
import { FilterElementComponent } from './components/result/when-loaded/filter-element/filter-element.component';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatRadioModule} from '@angular/material/radio';

@NgModule({
  declarations: [
    AppComponent,
    TakePhotoComponent,
    SendPhotoComponent,
    ProfileComponent,
    LoginComponent,
    RegistrationComponent,
    ResultComponent,
    MainComponent,
    MiniNavBarComponent,
    LoadBarComponent,
    WhenLoadedComponent,
    RecognitionCardComponent,
    FilterElementComponent
    // TextFieldComponent
  ],
  imports: [
    WebcamModule,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatFormFieldModule,
    FormsModule,
    HttpClientModule,
    MatIconModule,
    MatCheckboxModule,
    MatRadioModule
  ],
  providers: [PictureService, UserService],
  bootstrap: [AppComponent]
})
export class AppModule { }
