import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { notifier } from '../app';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin.html',
  styleUrl: './admin.scss',
})
export class Admin implements OnInit {
  apiUrl = 'http://127.0.0.1:8000';
  currentUser: any = null;
  
  // Sezione attiva
  activeTab: 'categorie' | 'utenti' | 'iscrizioni' = 'categorie';
  
  // ===== CATEGORIE =====
  categorie: any[] = [];
  nuovaCategoria = '';
  loadingCategorie = false;
  modalCategoriaEdit: any = null;
  categoriaEditNome = '';
  
  // ===== UTENTI =====
  utenti: any[] = [];
  loadingUtenti = false;
  modalUtenteEdit: any = null;
  ricercaUtenti = '';
  filtroAdminUtenti = '';
  
  // ===== ISCRIZIONI =====
  iscrizioni: any[] = [];
  loadingIscrizioni = false;
  nuovaIscrizioneIdEvento: any = null;
  nuovaIscrizioneIdUtente: any = null;
  ricercaIscrizioni = '';
  filtroIdEvento: any = null;
  filtroIdUtente: any = null;

  constructor(private http: HttpClient, private router: Router) {}

  // Metodo per ottenere gli header con fallback X-Session-ID
  private getHttpOptions() {
    let userData = sessionStorage.getItem('user');
    if (!userData) {
      userData = localStorage.getItem('user');
    }
    
    const options: any = { withCredentials: true };
    
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user.ID_UTENTE) {
          options.headers = {
            'X-Session-ID': user.ID_UTENTE.toString()
          };
        }
      } catch (e) {}
    }
    
    return options;
  }

  ngOnInit() {
    let userData = sessionStorage.getItem('user');
    if (!userData) {
      userData = localStorage.getItem('user');
    }
    
    if (userData) {
      this.currentUser = JSON.parse(userData);
      if (!this.currentUser.CHECK_ADMIN) {
        this.router.navigate(['/home']);
        return;
      }
    } else {
      this.router.navigate(['/login']);
      return;
    }

    this.loadCategorie();
    this.loadUtenti();
    this.loadIscrizioni();
  }

  // ===== CATEGORIE =====
  
  loadCategorie() {
    this.loadingCategorie = true;
    this.http.get<any>(`${this.apiUrl}/CATEGORIE`, this.getHttpOptions()).subscribe({
      next: (response: any) => {
        this.categorie = response?.categorie || [];
        this.loadingCategorie = false;
      },
      error: (err) => {
        notifier.error('Errore nel caricamento categorie');
        this.loadingCategorie = false;
      }
    });
  }

  creaCategoria() {
    if (!this.nuovaCategoria.trim()) {
      notifier.error('Inserisci il nome della categoria');
      return;
    }

    this.loadingCategorie = true;
    const data = { NOME_CATEGORIA: this.nuovaCategoria };
    
    this.http.post<any>(`${this.apiUrl}/CATEGORIE`, data, this.getHttpOptions()).subscribe({
      next: (response) => {
        notifier.success('Categoria creata con successo');
        this.nuovaCategoria = '';
        this.loadingCategorie = false;
        this.loadCategorie();
      },
      error: (err) => {
        const errorMsg = err.error?.detail || 'Errore nella creazione della categoria';
        notifier.error(errorMsg);
        this.loadingCategorie = false;
      }
    });
  }

  openEditCategoria(categoria: any) {
    this.modalCategoriaEdit = categoria;
    this.categoriaEditNome = categoria.NOME_CATEGORIA;
  }

  saveCategoria() {
    if (!this.categoriaEditNome.trim()) {
      notifier.error('Il nome non può essere vuoto');
      return;
    }

    this.loadingCategorie = true;
    const data = { NOME_CATEGORIA: this.categoriaEditNome };
    
    this.http.put<any>(`${this.apiUrl}/CATEGORIE/${this.modalCategoriaEdit.ID_CATEGORIA}`, data, this.getHttpOptions()).subscribe({
      next: () => {
        notifier.success('Categoria aggiornata con successo');
        this.loadingCategorie = false;
        this.closeModalCategoria();
        this.loadCategorie();
      },
      error: (err) => {
        const errorMsg = err.error?.detail || 'Errore nell\'aggiornamento della categoria';
        notifier.error(errorMsg);
        this.loadingCategorie = false;
      }
    });
  }

  eliminaCategoria(id: number, nome: string) {
    if (!confirm(`Elimina la categoria "${nome}"?`)) {
      return;
    }

    this.http.delete<any>(`${this.apiUrl}/CATEGORIE/${id}`, this.getHttpOptions()).subscribe({
      next: () => {
        notifier.success('Categoria eliminata con successo');
        this.loadCategorie();
      },
      error: (err) => {
        const errorMsg = err.error?.detail || 'Errore nell\'eliminazione della categoria';
        notifier.error(errorMsg);
      }
    });
  }

  closeModalCategoria() {
    this.modalCategoriaEdit = null;
    this.categoriaEditNome = '';
  }

  // migrated to NotificationService

  // ===== UTENTI =====

  loadUtenti() {
    this.loadingUtenti = true;
    let url = `${this.apiUrl}/UTENTI`;
    const params = [];
    if (this.ricercaUtenti.trim()) {
      params.push(`RICERCA=${encodeURIComponent(this.ricercaUtenti)}`);
    }
    if (this.filtroAdminUtenti) {
      params.push(`ADMIN=${this.filtroAdminUtenti}`);
    }
    if (params.length > 0) {
      url += '?' + params.join('&');
    }

    this.http.get<any>(url, this.getHttpOptions()).subscribe({
      next: (response: any) => {
        this.utenti = response?.utenti || [];
        this.loadingUtenti = false;
      },
      error: (err) => {
        notifier.error('Errore nel caricamento utenti');
        this.loadingUtenti = false;
      }
    });
  }

  openEditUtente(utente: any) {
    this.modalUtenteEdit = { ...utente };
  }

  saveUtente() {
    this.loadingUtenti = true;
    // Admin non può modificare l'email: non la inviamo nel payload
    const data = {
      NOME_UTENTE: this.modalUtenteEdit.NOME_UTENTE,
      CHECK_ADMIN: this.modalUtenteEdit.CHECK_ADMIN,
      INDIRIZZO_UTENTE: this.modalUtenteEdit.INDIRIZZO_UTENTE
    };

    
    this.http.put<any>(`${this.apiUrl}/UTENTI/${this.modalUtenteEdit.ID_UTENTE}`, data, this.getHttpOptions()).subscribe({
      next: () => {
        notifier.success('Utente aggiornato con successo');
        this.loadingUtenti = false;
        this.closeModalUtente();
        this.loadUtenti();
      },
      error: (err) => {
        const errorMsg = err.error?.detail || 'Errore nell\'aggiornamento dell\'utente';
        notifier.error(errorMsg);
        this.loadingUtenti = false;
      }
    });
  }

  eliminaUtente(id: number, nome: string) {
    if (!confirm(`Elimina l'utente "${nome}"? Questa azione non può essere annullata.`)) {
      return;
    }

    this.http.delete<any>(`${this.apiUrl}/UTENTI/${id}`, this.getHttpOptions()).subscribe({
      next: () => {
        notifier.success('Utente eliminato con successo');
        this.loadUtenti();
      },
      error: (err) => {
        const errorMsg = err.error?.detail || 'Errore nell\'eliminazione dell\'utente';
        notifier.error(errorMsg);
      }
    });
  }

  closeModalUtente() {
    this.modalUtenteEdit = null;
  }

  // migrated to NotificationService

  applicaFiltriUtenti() {
    this.loadUtenti();
  }

  resetFiltriUtenti() {
    this.ricercaUtenti = '';
    this.filtroAdminUtenti = '';
    this.loadUtenti();
  }

  // ===== ISCRIZIONI =====

  loadIscrizioni() {
    this.loadingIscrizioni = true;
    let url = `${this.apiUrl}/ISCRIZIONI`;
    const params = [];
    if (this.filtroIdEvento != null && String(this.filtroIdEvento).trim()) {
      params.push(`ID_EVENTO=${this.filtroIdEvento}`);
    }
    if (this.filtroIdUtente != null && String(this.filtroIdUtente).trim()) {
      params.push(`ID_UTENTE=${this.filtroIdUtente}`);
    }
    if (params.length > 0) {
      url += '?' + params.join('&');
    }

    this.http.get<any>(url, this.getHttpOptions()).subscribe({
      next: (response: any) => {
        this.iscrizioni = response?.iscrizioni || [];
        this.loadingIscrizioni = false;
      },
      error: (err) => {
        notifier.error('Errore nel caricamento iscrizioni');
        this.loadingIscrizioni = false;
      }
    });
  }

  creaIscrizione() {
    const idEvento = Number(this.nuovaIscrizioneIdEvento);
    const idUtente = Number(this.nuovaIscrizioneIdUtente);
    
    if (!idEvento || !idUtente) {
      notifier.error('Inserisci ID evento e ID utente validi');
      return;
    }

    this.loadingIscrizioni = true;
    const data = {};
    
    this.http.post<any>(
      `${this.apiUrl}/ISCRIZIONI/${idEvento}/${idUtente}`,
      data,
      this.getHttpOptions()
    ).subscribe({
      next: () => {
        notifier.success('Iscrizione creata con successo');
        this.nuovaIscrizioneIdEvento = null;
        this.nuovaIscrizioneIdUtente = null;
        this.loadingIscrizioni = false;
        this.loadIscrizioni();
      },
      error: (err) => {
        const errorMsg = err.error?.detail || 'Errore nella creazione dell\'iscrizione';
        notifier.error(errorMsg);
        this.loadingIscrizioni = false;
      }
    });
  }

  eliminaIscrizione(idEvento: number, idUtente: number) {
    if (!confirm(`Elimina l'iscrizione dell'utente ${idUtente} all'evento ${idEvento}?`)) {
      return;
    }

    this.http.delete<any>(
      `${this.apiUrl}/ISCRIZIONI/${idEvento}/${idUtente}`,
      this.getHttpOptions()
    ).subscribe({
      next: () => {
        notifier.success('Iscrizione eliminata con successo');
        this.loadIscrizioni();
      },
      error: (err) => {
        const errorMsg = err.error?.detail || 'Errore nell\'eliminazione dell\'iscrizione';
        notifier.error(errorMsg);
      }
    });
  }

  applicaFiltriIscrizioni() {
    this.loadIscrizioni();
  }

  resetFiltriIscrizioni() {
    this.filtroIdEvento = '';
    this.filtroIdUtente = '';
    this.loadIscrizioni();
  }

  // migrated to NotificationService
}

