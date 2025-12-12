import { Component, signal, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router, CanActivateFn } from '@angular/router';
import { CommonModule } from '@angular/common';
import { routes } from './app.routes';
import { inject } from '@angular/core';

// Auth Guard per proteggere le rotte
export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const userStr = sessionStorage.getItem('user');
  
  if (userStr) {
    return true;
  } else {
    router.navigate(['/login']);
    return false;
  }
};

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrls: ['./app.scss'],
})
export class App implements OnInit {
  protected readonly title = signal('FRONTEND');
  isLoggedIn = signal(false);
  isMenuOpen = signal(false);

  // Sections generated from the routes config (exclude empty and wildcard and login)
  readonly sections = routes
    .filter((r) => typeof r.path === 'string' && r.path !== '**' && r.path !== '' && r.path !== 'login')
    .map((r) => {
      const p = r.path as string;
      return { label: p.charAt(0).toUpperCase() + p.slice(1), path: '/' + p };
    });

  constructor(private router: Router) {}

  ngOnInit() {
    // Verifica se utente è loggato da sessionStorage
    this.checkLoginStatus();
    // Ricontrolla ogni volta che torna al componente
    window.addEventListener('focus', () => this.checkLoginStatus());
  }

  private checkLoginStatus() {
    const userStr = sessionStorage.getItem('user');
    this.isLoggedIn.set(!!userStr);
  }

  onProfileClick(e: Event) {
    e.preventDefault();
    const userStr = sessionStorage.getItem('user');
    if (!userStr) {
      this.router.navigate(['/login']);
    } else {
      this.router.navigate(['/profile']);
    }
    this.closeMenu();
  }

  toggleMenu() {
    this.isMenuOpen.update(v => !v);
  }

  closeMenu() {
    this.isMenuOpen.set(false);
  }
}
