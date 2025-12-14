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
  selector: 'app-profile',
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.html',
  styleUrl: './profile.scss',
})
export class Profile implements OnInit {
  user: User | null = null;
  apiUrl = 'http://127.0.0.1:8000';
  loading = false;
  isEditing = false;
  editData = {
    NOME_UTENTE: '',
    EMAIL_UTENTE: '',
    INDIRIZZO_UTENTE: '',
    PASSWORD_ATTUALE: '',
    PASSWORD_NUOVA: '',
    PASSWORD_NUOVA_CONFERMA: ''
  };
  // messages are shown via NotificationService (global)

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    // Recupera i dati utente da sessionStorage
    const userData = sessionStorage.getItem('user');
    if (userData) {
      this.user = JSON.parse(userData);
      this.initEditForm();
    } else {
      // Se non loggato, reindirizza al login
      this.router.navigate(['/login']);
    }
  }

  private initEditForm() {
    if (this.user) {
      this.editData = {
        NOME_UTENTE: this.user.NOME_UTENTE || '',
        EMAIL_UTENTE: this.user.EMAIL_UTENTE || '',
        INDIRIZZO_UTENTE: this.user.INDIRIZZO_UTENTE || '',
        PASSWORD_ATTUALE: '',
        PASSWORD_NUOVA: '',
        PASSWORD_NUOVA_CONFERMA: ''
      };
    }
  }

  /**
   * Attiva/disattiva modalità edit
   */
  toggleEdit() {
    this.isEditing = !this.isEditing;
    if (!this.isEditing) {
      this.initEditForm();
      notifier.clear();
    }
  }

  /**
   * Salva le modifiche al profilo
   */
  saveProfile() {
    if (!this.user) return;

    // Validazione password
    if (this.editData.PASSWORD_NUOVA || this.editData.PASSWORD_NUOVA_CONFERMA) {
      if (!this.editData.PASSWORD_ATTUALE) {
        notifier.error('Inserisci la password attuale per cambiare password');
        this.loading = false;
        return;
      }
      if (this.editData.PASSWORD_NUOVA !== this.editData.PASSWORD_NUOVA_CONFERMA) {
        notifier.error('Le nuove password non corrispondono');
        this.loading = false;
        return;
      }
      if (this.editData.PASSWORD_NUOVA.length < 6) {
        notifier.error('La nuova password deve avere almeno 6 caratteri');
        this.loading = false;
        return;
      }
    }

    this.loading = true;
    
    // Filtra i campi vuoti - NON includere ID_UTENTE nel body, è nel URL
    const updateData: any = {
      PASSWORD_ATTUALE: this.editData.PASSWORD_ATTUALE  // Invia password attuale sempre per autenticazione
    };
    
    if (this.editData.NOME_UTENTE && this.editData.NOME_UTENTE !== this.user.NOME_UTENTE) {
      updateData.NOME_UTENTE = this.editData.NOME_UTENTE;
    }
    if (this.editData.EMAIL_UTENTE && this.editData.EMAIL_UTENTE !== this.user.EMAIL_UTENTE) {
      updateData.EMAIL_UTENTE = this.editData.EMAIL_UTENTE;
    }
    if (this.editData.INDIRIZZO_UTENTE && this.editData.INDIRIZZO_UTENTE !== this.user.INDIRIZZO_UTENTE) {
      updateData.INDIRIZZO_UTENTE = this.editData.INDIRIZZO_UTENTE;
    }
    if (this.editData.PASSWORD_NUOVA) {
      updateData.PASSWORD_UTENTE = this.editData.PASSWORD_NUOVA;
    }

    // Se non ci sono modifiche (solo PASSWORD_ATTUALE per autenticazione, nessun campo da aggiornare)
    if (Object.keys(updateData).length === 1 && updateData.PASSWORD_ATTUALE) {
      notifier.error('Nessuna modifica da salvare');
      this.loading = false;
      return;
    }

    this.http.put<any>(`${this.apiUrl}/UTENTI/${this.user.ID_UTENTE}`, updateData, { withCredentials: true }).subscribe({
      next: (response) => {
        notifier.success(response.message);
        // Aggiorna i dati locali
        this.user = response.utente;
        sessionStorage.setItem('user', JSON.stringify(response.utente));
        this.initEditForm();
        this.isEditing = false;
        this.loading = false;
      },
      error: (err: HttpErrorResponse) => {
        let errorMsg = 'Errore nell\'aggiornamento del profilo';
        if (err.error?.message) {
          errorMsg = err.error.message;
        }
        notifier.error(errorMsg);
        this.loading = false;
      }
    });
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
        localStorage.removeItem('user');
        notifier.success('Logout eseguito');
        this.loading = false;
        // Reindirizza al login
        this.router.navigate(['/login']);
      },
      error: () => {
        // Comunque cancella la sessione locale
        sessionStorage.removeItem('user');
        localStorage.removeItem('user');
        notifier.success('Logout eseguito');
        this.loading = false;
        this.router.navigate(['/login']);
      }
    });
  }

  // messages routed via NotificationService
}
