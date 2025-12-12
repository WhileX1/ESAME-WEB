import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Login } from './login/login';
import { Profile } from './profile/profile';
import { authGuard } from './app';

export const routes: Routes = [
  
	{path: "" , redirectTo: 'home', pathMatch: 'full'},
	{path: 'home', component: Home},
	{path: 'login', component: Login},
	{path: 'profile', component: Profile, canActivate: [authGuard]}
];
