import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
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
  imports: [CommonModule, FormsModule],
  templateUrl: './home.html',
  styleUrls: ['./home.scss'],
})
export class Home implements OnInit {
  // Filter state
  maggiorenni = false;
  hasPassword = false;
  dateFrom: string | null = null;
  dateTo: string | null = null; // can be null = illimitato
  // price filter expressed as operator + value
  priceOp: string = '';// '<' | '>' | '=' | 'range' | ''
  priceVal: number | null = null;
  priceValMax: number | null = null; // Per range min_max
  categoria: string | null = '';
  ricerca: string | null = '';
  ordinamento: string = ''; // '' | 'asc' | 'desc'

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

  apiUrl = 'https://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  ngOnInit() {
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
    this.http.get<any>(url).subscribe({
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
    const alfabeto = this.convertOrdinamento(this.ordinamento);
    if (alfabeto) {
      params.push(`ALFABETO=${alfabeto}`);
    }

    url += params.join('&');

    // Call API
    this.http.get<EventoResponse>(url).subscribe({
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

  resetFilters() {
    this.maggiorenni = false;
    this.dateFrom = null;
    this.dateTo = null;
    this.priceOp = '';
    this.priceVal = null;
    this.priceValMax = null;
    this.categoria = '';
    this.ricerca = '';
    this.ordinamento = '';
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
}
