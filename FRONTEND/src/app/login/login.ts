import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { notifier } from '../app';

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
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login implements OnInit {
  // Mode toggle
  isLoginMode = true;
  
  // Login form
  loginEmail = '';
  loginPassword = '';
  
  // Registration form
  registerEmail = '';
  registerPassword = '';
  registerConfirmPassword = '';
  registerName = '';
  registerAddress = '';
  registerIsAdmin = false;
  registerAdminPassword = '';
  
  // UI state
  loading = false;
  
  apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {}

  /**
   * Cambia tra login e registrazione
   */
  toggleMode() {
    this.isLoginMode = !this.isLoginMode;
    this.clearMessages();
    this.clearForms();
  }

  /**
   * Effettua il login
   */
  async login() {
    if (!this.loginEmail || !this.loginPassword) {
      notifier.error('Inserisci email e password');
      return;
    }

    this.loading = true;
    const loginData = {
      EMAIL_UTENTE: this.loginEmail,
      PASSWORD_UTENTE: this.loginPassword
    };

    this.http.post<any>(`${this.apiUrl}/LOGIN`, loginData, { withCredentials: true }).subscribe({
      next: (response) => {
        notifier.success(response.message);
        this.loading = false;
        
        // Salva i dati utente in sessionStorage E localStorage
        sessionStorage.setItem('user', JSON.stringify(response.utente));
        localStorage.setItem('user', JSON.stringify(response.utente));
        
        // Reindirizza al profilo dopo 1 secondo
        setTimeout(() => {
          this.router.navigate(['/profile']);
        }, 1000);
      },
      error: (err: HttpErrorResponse) => {
        let errorMsg = 'Errore di login';
        if (err.status === 401) {
          errorMsg = 'Credenziali non valide';
        } else if (err.error?.message) {
          errorMsg = err.error.message;
        }
        notifier.error(errorMsg);
        this.loading = false;
      }
    });
  }

  /**
   * Effettua la registrazione
   */
  async register() {
    // Validazione form
    if (!this.registerEmail || !this.registerPassword || !this.registerConfirmPassword || !this.registerName) {
      notifier.error('Completa tutti i campi obbligatori');
      return;
    }

    if (this.registerPassword !== this.registerConfirmPassword) {
      notifier.error('Le password non corrispondono');
      return;
    }

    if (this.registerPassword.length < 6) {
      notifier.error('La password deve avere almeno 6 caratteri');
      return;
    }

    if (!this.registerAddress) {
      notifier.error('Inserisci un indirizzo');
      return;
    }

    this.loading = true;

    const registerData: any = {
      EMAIL_UTENTE: this.registerEmail,
      PASSWORD_UTENTE: this.registerPassword,
      NOME_UTENTE: this.registerName,
      INDIRIZZO_UTENTE: this.registerAddress,
      CHECK_ADMIN: this.registerIsAdmin ? 1 : 0
    };

    // Se admin, aggiungi password admin
    if (this.registerIsAdmin) {
      if (!this.registerAdminPassword) {
        notifier.error('Inserisci la password amministratore');
        this.loading = false;
        return;
      }
      registerData.ADMIN_PASSWORD = this.registerAdminPassword;
    }

    this.http.post<any>(`${this.apiUrl}/UTENTI`, registerData, { withCredentials: true }).subscribe({
      next: (response) => {
        notifier.success(response.message);
        
        // Auto-login dopo registrazione
        setTimeout(() => {
          this.loginEmail = this.registerEmail;
          this.loginPassword = this.registerPassword;
          this.toggleMode();
          this.login();
        }, 1500);
      },
      error: (err: HttpErrorResponse) => {
        let errorMsg = 'Errore di registrazione';
        if (err.error?.message) {
          errorMsg = err.error.message;
        }
        notifier.error(errorMsg);
        this.loading = false;
      }
    });
  }

  /**
   * Mostra messaggio
   */
  /**
   * Cancella messaggi globali
   */
  private clearMessages() {
    notifier.clear();
  }

  /**
   * Cancella form
   */
  private clearForms() {
    this.loginEmail = '';
    this.loginPassword = '';
    this.registerEmail = '';
    this.registerPassword = '';
    this.registerConfirmPassword = '';
    this.registerName = '';
    this.registerAddress = '';
    this.registerIsAdmin = false;
    this.registerAdminPassword = '';
  }
}
