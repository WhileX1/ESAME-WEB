import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
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
  message: { type: 'success' | 'error', text: string } | null = null;
  
  apiUrl = 'https://127.0.0.1:8000';

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
      this.showMessage('error', 'Inserisci email e password');
      return;
    }

    this.loading = true;
    const loginData = {
      EMAIL_UTENTE: this.loginEmail,
      PASSWORD_UTENTE: this.loginPassword
    };

    console.log('🔐 Tentativo di login...', loginData);

    this.http.post<any>(`${this.apiUrl}/LOGIN`, loginData).subscribe({
      next: (response) => {
        this.showMessage('success', response.message);
        console.log('✅ Login riuscito:', response.utente);
        
        // Salva i dati utente in sessionStorage
        sessionStorage.setItem('user', JSON.stringify(response.utente));
        
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
        this.showMessage('error', errorMsg);
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
      this.showMessage('error', 'Completa tutti i campi obbligatori');
      return;
    }

    if (this.registerPassword !== this.registerConfirmPassword) {
      this.showMessage('error', 'Le password non corrispondono');
      return;
    }

    if (this.registerPassword.length < 6) {
      this.showMessage('error', 'La password deve avere almeno 6 caratteri');
      return;
    }

    if (!this.registerAddress) {
      this.showMessage('error', 'Inserisci un indirizzo');
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
        this.showMessage('error', 'Inserisci la password amministratore');
        this.loading = false;
        return;
      }
      registerData.ADMIN_PASSWORD = this.registerAdminPassword;
    }

    console.log('📝 Tentativo di registrazione...', registerData);

    this.http.post<any>(`${this.apiUrl}/UTENTI`, registerData).subscribe({
      next: (response) => {
        this.showMessage('success', response.message);
        console.log('✅ Registrazione riuscita:', response.utente);
        
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
        this.showMessage('error', errorMsg);
        this.loading = false;
      }
    });
  }

  /**
   * Mostra messaggio
   */
  private showMessage(type: 'success' | 'error', text: string) {
    this.message = { type, text };
    console.log(`${type === 'success' ? '✅' : '❌'} ${text}`);
  }

  /**
   * Cancella messaggi
   */
  private clearMessages() {
    this.message = null;
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
