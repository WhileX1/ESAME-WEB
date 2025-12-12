import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';

interface User {
  ID_UTENTE: number;
  EMAIL_UTENTE: string;
  NOME_UTENTE: string;
  CHECK_ADMIN: boolean;
  DATA_REGISTRAZIONE: string;
  INDIRIZZO_UTENTE?: string;
  COORDINATE_UTENTE?: string;
}

@Component({
  selector: 'app-profile',
  imports: [CommonModule],
  templateUrl: './profile.html',
  styleUrl: './profile.scss',
})
export class Profile implements OnInit {
  user: User | null = null;
  apiUrl = 'https://127.0.0.1:8000';
  loading = false;

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    // Recupera i dati utente da sessionStorage
    const userData = sessionStorage.getItem('user');
    if (userData) {
      this.user = JSON.parse(userData);
    } else {
      // Se non loggato, reindirizza al login
      this.router.navigate(['/login']);
    }
  }

  /**
   * Logout dell'utente
   */
  logout() {
    this.loading = true;
    this.http.get<any>(`${this.apiUrl}/LOGOUT`, { withCredentials: true }).subscribe({
      next: () => {
        // Cancella i dati della sessione
        sessionStorage.removeItem('user');
        // Reindirizza al login
        this.router.navigate(['/login']);
      },
      error: (err: HttpErrorResponse) => {
        // Comunque cancella la sessione locale
        sessionStorage.removeItem('user');
        this.router.navigate(['/login']);
      }
    });
  }
}
