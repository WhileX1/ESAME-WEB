import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { routes } from './app.routes';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrls: ['./app.scss'],
})
export class App {
  protected readonly title = signal('FRONTEND');
  isLoggedIn = signal(false);
  isMenuOpen = signal(false);

  // Sections generated from the routes config (exclude empty and wildcard and login)
  readonly sections = routes
    .filter((r) => typeof r.path === 'string' && r.path !== '**' && r.path !== '' && r.path !== 'login')
    .map((r) => {
      const p = r.path as string;
      return { label: p.charAt(0).toUpperCase() + p.slice(1), path: '/' + p };
    })
    .concat([{ label: 'Profile', path: '/profile' }]); // Sempre mostra Profile

  constructor(private router: Router) {}

  onProfileClick(e: Event) {
    e.preventDefault();
    if (!this.isLoggedIn()) {
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
