import { Component, OnInit } from '@angular/core';
import { CommonModule, NgIf, NgForOf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

export interface Filters {
  maggiorenni: boolean;
  dateFrom?: string | null;
  dateTo?: string | null;
  PREZZO?: string | null; // format: '<10', '>20', '=15' or null
  categoria?: string | null;
  ricerca?: string | null;
  ordinamento?: string | null; // 'asc' | 'desc' | null
}

export interface EventoResponse {
  risultati: number;
  eventi: any[];
  filtri: {
    ID_UTENTE: number | null;
    ISCRITTO: boolean | null;
    MAGGIORENNI: boolean | null;
    DATA: string | null;
    ALFABETO: string | null;
    PREZZO: string | null;
    CATEGORIA: string | null;
    DISTANZA: string | null;
    RICERCA: string | null;
  };
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, NgIf, NgForOf, FormsModule],
  templateUrl: './home.html',
  styleUrls: ['./home.scss'],
})
export class Home implements OnInit {
  // Filter state
  maggiorenni = '';  // '' = no filter, 'true'/'false' = filtered
  hasPassword = '';  // '' = no filter, 'true'/'false' = filtered
  dateFrom: string | null = null;
  dateTo: string | null = null; // can be null = illimitato
  // price filter expressed as operator + value
  priceOp: string = '';// '<' | '>' | '=' | 'range' | ''
  priceVal: number | null = null;
  priceValMax: number | null = null; // Per range min_max
  categoria: string | null = '';
  ricerca: string | null = '';
  ordinamento: string = ''; // '' | 'asc' | 'desc'
  
  // Filtri per utente loggato
  iscritto: boolean | null = null;
  creatoDaMe: boolean | null = null;
  distanzaOp: string = ''; // '<' | '>' | '=' | 'range' | ''
  distanzaVal: number | null = null;
  distanzaValMax: number | null = null; // Per range min_max
  
  // User session
  currentUser: any = null;

  // API response data
  eventi: any[] = [];
  loading = false;
  error: string | null = null;

  // Scroll to top button
  showScrollButton = false;

  // Debounce timer
  private debounceTimer: any = null;

  // Categories from backend
  categories = [
    { value: '', label: 'Tutte' }
  ];

  // Modal state
  showModal = false;
  selectedEventId: number | null = null;
  selectedEventDetail: any = null;
  modalLoading = false;
  modalError: string | null = null;
  modalSuccess: string | null = null;
  userIscritto = false;
  iscrittiBtnLoading = false;
  eventPassword: string = '';
  // iscrizioni list for event owner/admin
  showIscrizioniList = false;
  iscrizioniList: Array<any> = [];
  iscrizioniLoading = false;
  iscrizioniError: string | null = null;
  // create event modal state and form fields
  showCreateModal = false;
  createLoading = false;
  createError: string | null = null;
  newNomeEvento = '';
  newDescrizioneEvento = '';
  newDataEvento = '';
  newIndirizzoEvento = '';
  newCoordinateEvento = '';
  newCostoEvento: number | null = null;
  newMaxPartecipanti: number | null = null;
  newCheckMaggiorenni = false;
  newPasswordEvento = '';
  newCategoria1: string | null = '';
  newCategoria2: string | null = '';
  newCategoria3: string | null = '';

  apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient, private router: Router) {}

  navigateToLogin() {
    // Close modal then navigate to login
    try { this.closeEventModal(); } catch (e) {}
    this.router.navigate(['/login']);
  }

  ngOnInit() {
    // Recupera l'utente da sessionStorage o localStorage se loggato
    let userData = sessionStorage.getItem('user');
    if (!userData) {
      userData = localStorage.getItem('user');
    }
    if (userData) {
      this.currentUser = JSON.parse(userData);
    }
    
    // Carica le categorie e gli eventi al caricamento della pagina
    this.loadCategories();
    this.applyFilters();
    
    // Listen to scroll events on .app-main container
    setTimeout(() => {
      const appMain = document.querySelector('.app-main');
      if (appMain) {
        appMain.addEventListener('scroll', () => {
          this.showScrollButton = (appMain as HTMLElement).scrollTop > 300;
        });
      }
    }, 0);
  }

  /**
   * Carica le categorie dal backend
   */
  private loadCategories() {
    const url = `${this.apiUrl}/CATEGORIE`;
    this.http.get<any>(url, { withCredentials: true }).subscribe({
      next: (response: any) => {
        // Costruisci array categorie con 'Tutte' come prima opzione
        this.categories = [
          { value: '', label: 'Tutte' },
          ...response.categorie.map((cat: any) => ({
            value: cat.NOME_CATEGORIA,
            label: cat.NOME_CATEGORIA
          }))
        ];
      },
      error: (err: any) => {
        // Mantieni solo 'Tutte' in caso di errore
      }
    });
  }

  /**
   * Converte il formato date HTML (YYYY-MM-DD) al formato backend (DD-MM-YYYY)
   */
  private convertDateFormat(dateString: string | null): string | null {
    if (!dateString) return null;
    const [year, month, day] = dateString.split('-');
    return `${day}-${month}-${year}`;
  }

  /**
   * Converte ordinamento da asc/desc a > / <
   */
  private convertOrdinamento(ord: string): string | null {
    if (ord === 'asc') return '>';    // A → Z
    if (ord === 'desc') return '<';   // Z → A
    return null;
  }

  // Called whenever a filter changes
  applyFilters() {
    // Clear previous timer
    if (this.debounceTimer) {
      clearTimeout(this.debounceTimer);
    }

    // Set new timer - wait 500ms before making the API call
    this.debounceTimer = setTimeout(() => {
      this.executeFilters();
    }, 500);
  }

  // Execute the actual filter API call
  private executeFilters() {
    this.loading = true;
    this.error = null;

    // Build PREZZO according to backend format: <value, >value, =value or range min_max
    let prezzo: string | null = null;
    if (this.priceVal != null) {
      if (this.priceOp === 'range') {
        // Range requires both min and max
        if (this.priceValMax == null) {
          this.error = 'Inserire il secondo valore del range';
          this.loading = false;
          return;
        }
        // Range format: 10_20
        prezzo = `${this.priceVal}_${this.priceValMax}`;
      } else if (this.priceOp === '=') {
        // Exact value: just the number without operator
        prezzo = this.priceVal.toString();
      } else if (this.priceOp && this.priceOp !== '') {
        // Operators < and >: concatenate directly
        prezzo = `${this.priceOp}${this.priceVal}`;
      }
    }

    // Build DISTANZA according to backend format: <value, >value, =value or range min_max
    let distanza: string | null = null;
    if (this.distanzaVal != null && this.currentUser) {
      if (this.distanzaOp === 'range') {
        // Range requires both min and max
        if (this.distanzaValMax == null) {
          this.error = 'Inserire il secondo valore del range per la distanza';
          this.loading = false;
          return;
        }
        // Range format: 10_20
        distanza = `${this.distanzaVal}_${this.distanzaValMax}`;
      } else if (this.distanzaOp === '=') {
        // Exact value: just the number without operator
        distanza = this.distanzaVal.toString();
      } else if (this.distanzaOp && this.distanzaOp !== '') {
        // Operators < and >: concatenate directly
        distanza = `${this.distanzaOp}${this.distanzaVal}`;
      }
    }

    // Convert date format from HTML (YYYY-MM-DD) to backend (DD-MM-YYYY)
    const dataFrom = this.convertDateFormat(this.dateFrom);
    const dataTo = this.convertDateFormat(this.dateTo);
    
    // Build DATA parameter: "DD-MM-YYYY_DD-MM-YYYY" or single date
    let dataParam: string | null = null;
    if (dataFrom && dataTo) {
      dataParam = `${dataFrom}_${dataTo}`;
    } else if (dataFrom) {
      dataParam = dataFrom;
    } else if (dataTo) {
      dataParam = dataTo;
    }

    // Build URL with query parameters
    let url = `${this.apiUrl}/EVENTI?`;
    const params: string[] = [];

    if (this.maggiorenni) {
      params.push(`MAGGIORENNI=${this.maggiorenni}`);
    }
    if (this.hasPassword) {
      params.push(`HAS_PASSWORD=${this.hasPassword}`);
    }
    if (dataParam) {
      params.push(`DATA=${encodeURIComponent(dataParam)}`);
    }
    if (prezzo) {
      params.push(`PREZZO=${prezzo}`);
    }
    if (this.categoria) {
      params.push(`CATEGORIA=${this.categoria}`);
    }
    if (this.ricerca) {
      params.push(`RICERCA=${encodeURIComponent(this.ricerca)}`);
    }
    if (this.currentUser) {
      // Aggiungi filtri per utente loggato - solo se true (checked)
      if (this.iscritto === true) {
        params.push(`ISCRITTO=true`);
      }
      if (this.creatoDaMe === true) {
        params.push(`CREATO_DA_ME=true`);
      }
      if (distanza) {
        params.push(`DISTANZA=${encodeURIComponent(distanza)}`);
      }
    }
    const alfabeto = this.convertOrdinamento(this.ordinamento);
    if (alfabeto) {
      params.push(`ALFABETO=${alfabeto}`);
    }

    url += params.join('&');

    // Prepara headers con X-Session-ID dal localStorage se disponibile
    const headers: any = {};
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user && user.ID_UTENTE) {
          headers['X-Session-ID'] = user.ID_UTENTE.toString();
        }
      } catch (e) {
        // Ignora errori di parsing
      }
    }

    // Call API
    this.http.get<EventoResponse>(url, { withCredentials: true, headers }).subscribe({
      next: (response: EventoResponse) => {
        this.eventi = response.eventi;
        this.loading = false;
      },
      error: (err: any) => {
        let errorMessage = 'Errore nel caricamento degli eventi';
        
        if (err.error?.detail) {
          errorMessage = err.error.detail;
        } else if (err.status === 0) {
          errorMessage = 'Impossibile raggiungere il backend. Verifica che sia in esecuzione su https://127.0.0.1:8000';
        } else if (err.status === 401) {
          errorMessage = 'Non autenticato. Effettua il login prima.';
        } else if (err.status === 403) {
          errorMessage = 'Accesso negato.';
        } else if (err.statusText) {
          errorMessage = `Errore ${err.status}: ${err.statusText}`;
        }
        
        this.error = errorMessage;
        this.loading = false;
      }
    });
  }

  // Clear priceValMax when priceOp changes
  onPriceOpChange() {
    // Se cambi da range a un altro operatore, svuota il MAX
    if (this.priceOp !== 'range') {
      this.priceValMax = null;
    }
    this.applyFilters();
  }

  // Clear distanzaValMax when distanzaOp changes
  onDistanzaOpChange() {
    // Se cambi da range a un altro operatore, svuota il MAX
    if (this.distanzaOp !== 'range') {
      this.distanzaValMax = null;
    }
    this.applyFilters();
  }

  resetFilters() {
    this.maggiorenni = '';
    this.hasPassword = '';
    this.dateFrom = null;
    this.dateTo = null;
    this.priceOp = '';
    this.priceVal = null;
    this.priceValMax = null;
    this.categoria = '';
    this.ricerca = '';
    this.ordinamento = '';
    // Reset user-specific filters
    this.iscritto = null;
    this.creatoDaMe = null;
    this.distanzaOp = '';
    this.distanzaVal = null;
    this.distanzaValMax = null;
    // Clear timer and execute immediately
    if (this.debounceTimer) {
      clearTimeout(this.debounceTimer);
    }
    this.executeFilters();
  }

  scrollToTop() {
    const appMain = document.querySelector('.app-main');
    if (appMain) {
      appMain.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  /**
   * Apre la modale e carica i dettagli dell'evento
   */
  openEventModal(eventId: number) {
    this.selectedEventId = eventId;
    this.showModal = true;
    this.modalLoading = true;
    this.modalError = null;
    this.selectedEventDetail = null;

    // Fetch event details
    const url = `${this.apiUrl}/EVENTI/${eventId}`;
    this.http.get<any>(url, { withCredentials: true }).subscribe({
      next: (response: any) => {
        this.selectedEventDetail = response.evento || response;
        this.modalLoading = false;
        this.modalError = null;
        this.modalSuccess = null;
        this.eventPassword = '';
        this.checkUserIscritto();
      },
      error: (err: any) => {
        let errorMessage = 'Errore nel caricamento dell\'evento';
        if (err.error?.detail) {
          errorMessage = err.error.detail;
        } else if (err.status === 0) {
          errorMessage = 'Impossibile raggiungere il backend';
        }
        this.modalError = errorMessage;
        this.modalLoading = false;
      }
    });
  }

  /**
   * Chiude la modale
   */
  closeEventModal() {
    this.showModal = false;
    this.selectedEventId = null;
    this.selectedEventDetail = null;
    this.modalLoading = false;
    this.modalError = null;
    this.modalSuccess = null;
    this.userIscritto = false;
  }

  /**
   * Controlla se l'utente è iscritto all'evento
   */
  checkUserIscritto() {
    if (!this.currentUser || !this.selectedEventId) {
      this.userIscritto = false;
      return;
    }

    const idUtente = this.currentUser.ID_UTENTE;
    const idEvento = this.selectedEventId;

    // Use query-based endpoint to avoid 404 when not subscribed
    const url = `${this.apiUrl}/ISCRIZIONI?ID_EVENTO=${idEvento}&ID_UTENTE=${idUtente}`;
    // include X-Session-ID header from localStorage if available to avoid 403 when cookies are not set
    const headers: any = {};
    const userData = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user && user.ID_UTENTE) headers['X-Session-ID'] = user.ID_UTENTE.toString();
      } catch (e) {}
    }
    this.http.get<any>(url, { withCredentials: true, headers }).subscribe({
      next: (resp: any) => {
        const arr = resp?.iscrizioni || [];
        this.userIscritto = arr.length > 0;
      },
      error: () => {
        // If request fails, assume not subscribed but avoid noisy stack traces
        this.userIscritto = false;
      }
    });
  }

  /**
   * Apri lista iscrizioni per l'evento (solo creatore o admin)
   */
  /**
   * Apri lista iscrizioni per l'evento (solo creatore o admin)
   * @param forceReload se true forza il reload dei dati anche se il pannello è già aperto
   */
  openIscrizioni(forceReload: boolean = false) {
    if (!this.currentUser || !this.selectedEventId) return;
    const idEvento = this.selectedEventId;

    // If panel is already open and no forced reload requested, just scroll to it and exit
    if (this.showIscrizioniList && !forceReload) {
      setTimeout(() => this.scrollToIscrizioniPanel(), 50);
      return;
    }

    this.showIscrizioniList = true;
    this.iscrizioniLoading = true;
    this.iscrizioniError = null;
    const headers: any = {};
    const userData = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user && user.ID_UTENTE) headers['X-Session-ID'] = user.ID_UTENTE.toString();
      } catch (e) {}
    }

    const url = `${this.apiUrl}/ISCRIZIONI?ID_EVENTO=${idEvento}`;
    this.http.get<any>(url, { withCredentials: true, headers }).subscribe({
      next: (resp: any) => {
        this.iscrizioniList = resp?.iscrizioni || [];
        this.iscrizioniLoading = false;
        // Scroll modal to show iscrizioni panel
        setTimeout(() => this.scrollToIscrizioniPanel(), 50);
      },
      error: (err: any) => {
        this.iscrizioniError = err?.error?.detail || 'Impossibile caricare le iscrizioni';
        this.iscrizioniLoading = false;
      }
    });
  }

  closeIscrizioni() {
    this.showIscrizioniList = false;
    this.iscrizioniList = [];
    this.iscrizioniError = null;
  }

  private scrollToIscrizioniPanel() {
    try {
      const modalScroll = document.querySelector('.modal-scroll') as HTMLElement | null;
      const panel = modalScroll?.querySelector('.iscrizioni-panel') as HTMLElement | null;
      if (modalScroll && panel) {
        modalScroll.scrollTo({ top: panel.offsetTop - 20, behavior: 'smooth' });
      }
    } catch (e) {}
  }

  // Open create event modal
  openCreateModal() {
    this.showCreateModal = true;
    this.createError = null;
    // reset fields
    this.newNomeEvento = '';
    this.newDescrizioneEvento = '';
    this.newDataEvento = '';
    this.newIndirizzoEvento = '';
    this.newCoordinateEvento = '';
    this.newCostoEvento = null;
    this.newMaxPartecipanti = null;
    this.newCheckMaggiorenni = false;
    this.newPasswordEvento = '';
    this.newCategoria1 = '';
    this.newCategoria2 = '';
    this.newCategoria3 = '';
  }

  closeCreateModal() {
    this.showCreateModal = false;
    this.createError = null;
    this.createLoading = false;
  }

  // Create event POST /EVENTI
  createEvento() {
    // require login to create an event
    if (!this.currentUser) {
      this.createError = 'Devi essere loggato per creare un evento.';
      return;
    }
    // basic client-side validation
    if (!this.newNomeEvento || !this.newDescrizioneEvento || !this.newDataEvento) {
      this.createError = 'Compila i campi obbligatori: nome, descrizione, data.';
      return;
    }

    this.createLoading = true;
    this.createError = null;

    const payload: any = {
      NOME_EVENTO: this.newNomeEvento,
      DESCRIZIONE_EVENTO: this.newDescrizioneEvento,
      DATA_EVENTO: this.newDataEvento
    };
    if (this.newIndirizzoEvento) payload.INDIRIZZO_EVENTO = this.newIndirizzoEvento;
    if (this.newCoordinateEvento) payload.COORDINATE_EVENTO = this.newCoordinateEvento;
    if (this.newCostoEvento != null) payload.COSTO = this.newCostoEvento;
    if (this.newMaxPartecipanti != null) payload.MAX_PARTECIPANTI = this.newMaxPartecipanti;
    if (this.newCheckMaggiorenni) payload.CHECK_MAGGIORENNI = 1;
    if (this.newPasswordEvento) payload.PASSWORD_EVENTO = this.newPasswordEvento;

    // include up to 3 selected categories
    const selectedCats: string[] = [];
    if (this.newCategoria1) selectedCats.push(this.newCategoria1);
    if (this.newCategoria2) selectedCats.push(this.newCategoria2);
    if (this.newCategoria3) selectedCats.push(this.newCategoria3);
    if (selectedCats.length > 0) payload.CATEGORIE = selectedCats;

    const headers: any = {};
    const userData = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user && user.ID_UTENTE) headers['X-Session-ID'] = user.ID_UTENTE.toString();
      } catch (e) {}
    }

    this.http.post<any>(`${this.apiUrl}/EVENTI`, payload, { withCredentials: true, headers }).subscribe({
      next: (resp: any) => {
        this.createLoading = false;
        this.showCreateModal = false;
        this.modalSuccess = 'Evento creato con successo.';
        setTimeout(() => this.modalSuccess = null, 3500);
        // refresh events
        try { this.executeFilters(); } catch (e) {}
      },
      error: (err: any) => {
        this.createLoading = false;
        this.createError = err?.error?.detail || err?.error?.message || 'Errore durante la creazione evento';
      }
    });
  }

  /**
   * Elimina iscrizione specifica (solo creatore/admin)
   */
  eliminaIscrizione(idUtente: number) {
    if (!this.selectedEventId) return;
    const idEvento = this.selectedEventId;
    const headers: any = {};
    const userData = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user && user.ID_UTENTE) headers['X-Session-ID'] = user.ID_UTENTE.toString();
      } catch (e) {}
    }
    this.http.delete<any>(`${this.apiUrl}/ISCRIZIONI/${idEvento}/${idUtente}`, { withCredentials: true, headers }).subscribe({
      next: () => {
        // remove from local list
        this.iscrizioniList = this.iscrizioniList.filter(i => i.ID_UTENTE !== idUtente);
        this.modalSuccess = 'Iscrizione rimossa.';
        setTimeout(() => this.modalSuccess = null, 3000);
      },
      error: (err: any) => {
        this.iscrizioniError = err?.error?.detail || 'Errore durante la cancellazione';
      }
    });
  }

  /**
   * Iscrive l'utente all'evento
   */
  iscrivitiAlEvento() {
    if (!this.currentUser || !this.selectedEventId) {
      this.modalError = 'Devi essere loggato per iscriverti';
      return;
    }

    this.iscrittiBtnLoading = true;
    const idUtente = this.currentUser.ID_UTENTE;
    const idEvento = this.selectedEventId;
    const data: any = {};
    if (this.eventPassword) data.PASSWORD_EVENTO = this.eventPassword;

    // include X-Session-ID header from localStorage/sessionStorage if available
    const headers: any = {};
    const userData = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user && user.ID_UTENTE) headers['X-Session-ID'] = user.ID_UTENTE.toString();
      } catch (e) {}
    }

    this.http.post<any>(
      `${this.apiUrl}/ISCRIZIONI/${idEvento}/${idUtente}`,
      data,
      { withCredentials: true, headers }
    ).subscribe({
      next: () => {
        this.userIscritto = true;
        this.iscrittiBtnLoading = false;
        this.modalError = null;
        this.modalSuccess = 'Iscrizione avvenuta con successo.';
        // Clear success message after a short time
        setTimeout(() => this.modalSuccess = null, 4000);
        // clear entered password
        this.eventPassword = '';
        // Refresh event list and iscrizioni list (if open)
        try { this.executeFilters(); } catch (e) {}
        if (this.showIscrizioniList) {
          this.openIscrizioni(true);
        }
      },
      error: (err: any) => {
        let errorMessage = 'Errore nell\'iscrizione';
        if (err.error?.detail) {
          errorMessage = err.error.detail;
        }
        this.modalError = errorMessage;
        this.iscrittiBtnLoading = false;
      }
    });
  }

  /**
   * Disiscrive l'utente dall'evento
   */
  disiscriviDalEvento() {
    if (!this.currentUser || !this.selectedEventId) {
      this.modalError = 'Devi essere loggato per disiscriverti';
      return;
    }

    this.iscrittiBtnLoading = true;
    const idUtente = this.currentUser.ID_UTENTE;
    const idEvento = this.selectedEventId;

    // include X-Session-ID header from localStorage/sessionStorage if available
    const headers: any = {};
    const userData = localStorage.getItem('user') || sessionStorage.getItem('user');
    if (userData) {
      try {
        const user = JSON.parse(userData);
        if (user && user.ID_UTENTE) headers['X-Session-ID'] = user.ID_UTENTE.toString();
      } catch (e) {}
    }

    this.http.delete<any>(
      `${this.apiUrl}/ISCRIZIONI/${idEvento}/${idUtente}`,
      { withCredentials: true, headers }
    ).subscribe({
      next: () => {
        this.userIscritto = false;
        this.iscrittiBtnLoading = false;
        this.modalError = null;
        this.modalSuccess = 'Disiscrizione avvenuta con successo.';
        // Clear success message after a short time
        setTimeout(() => this.modalSuccess = null, 4000);
        // Refresh event list and iscrizioni list (if open)
        try { this.executeFilters(); } catch (e) {}
        if (this.showIscrizioniList) {
          this.openIscrizioni(true);
        }
      },
      error: (err: any) => {
        let errorMessage = 'Errore nella disiscrizione';
        if (err.error?.detail) {
          errorMessage = err.error.detail;
        }
        this.modalError = errorMessage;
        this.iscrittiBtnLoading = false;
      }
    });
  }
}
