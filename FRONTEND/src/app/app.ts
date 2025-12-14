import { Component, signal, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router, CanActivateFn, NavigationEnd } from '@angular/router';
import { CommonModule, NgIf, NgForOf, AsyncPipe } from '@angular/common';
import { routes } from './app.routes';
import { inject } from '@angular/core';
import { filter } from 'rxjs';
import { BehaviorSubject } from 'rxjs';

// Simple notifier exported for global notifications (replaces notification.service.ts)
export type NotificationType = 'success' | 'error';
export interface NotificationPayload { type: NotificationType; text: string }
const notifierSubject = new BehaviorSubject<NotificationPayload | null>(null);
export const notifier = {
  message$: notifierSubject.asObservable(),
  success(text: string, autoDismissMs = 3500) { notifierSubject.next({ type: 'success', text }); if (autoDismissMs) setTimeout(() => notifierSubject.next(null), autoDismissMs); },
  error(text: string, autoDismissMs = 4500) { notifierSubject.next({ type: 'error', text }); if (autoDismissMs) setTimeout(() => notifierSubject.next(null), autoDismissMs); },
  clear() { notifierSubject.next(null); }
};

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
  imports: [CommonModule, NgIf, NgForOf, AsyncPipe, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrls: ['./app.scss'],
})
export class App implements OnInit {
  protected readonly title = signal('FRONTEND');
  isLoggedIn = signal(false);
  isMenuOpen = signal(false);
  currentUser: any = null;

  // Sections generated from the routes config (exclude empty and wildcard and login and admin)
  readonly sections = routes
    .filter((r) => typeof r.path === 'string' && r.path !== '**' && r.path !== '' && r.path !== 'login' && r.path !== 'admin')
    .map((r) => {
      const p = r.path as string;
      return { label: p.charAt(0).toUpperCase() + p.slice(1), path: '/' + p };
    });

  constructor(private router: Router) {}

  // expose notification stream for the root template
  message$ = notifier.message$;

  ngOnInit() {
    // Verifica se utente è loggato da sessionStorage
    this.checkLoginStatus();
    // Ricontrolla ogni volta che torna al componente
    window.addEventListener('focus', () => this.checkLoginStatus());
    // Ricontrolla dopo ogni navigazione
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => this.checkLoginStatus());
  }

  private checkLoginStatus() {
    const userStr = sessionStorage.getItem('user');
    this.isLoggedIn.set(!!userStr);
    if (userStr) {
      this.currentUser = JSON.parse(userStr);
    } else {
      this.currentUser = null;
    }
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
