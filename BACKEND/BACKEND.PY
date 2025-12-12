#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| PROGETTO DI SVIATOSLAV SAPIZHAK |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# pip install "fastapi"
# pip install uvicorn
# pip install itsdangerous
# python -m uvicorn Main.py:app --reload

from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException

import mysql.connector
from datetime import date

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

#----------------------------------------------------------------\
import urllib.parse # Per l'encoding dell'URL                     | USATO PER I COMMENTI
# urllib.parse.quote('pippo@example.com') => 'pippo%40example.com'| CLICCABILI
#----------------------------------------------------------------/

# SESSIONE
from starlette.middleware.sessions import SessionMiddleware  

# AGGIUNTA AL MIDDLEWARE 
import logging

# CLASSI SPECIFICHE PER EVITARE L'ERRORE DI CONVERSIONE
from datetime import datetime, date  

# MODIFICA A SCELTA DEGLI ATTRIBUTI (PUT)
from typing import Optional

# DECIMAL => CONVERSIONE IN FLOAT
from decimal import Decimal

# HASHING DELLE PASSWORD
# pip install bcrypt
import bcrypt

# ESPRESSIONI REGOLARI
import re

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| ADMIN PASSWORD .env |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#    
                         
import os                                                           #   🡸 PER VARIABILE D'AMBIENTE
# pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()                                                       #   🡸 CARICA VARIABILI DA .env
# 🚨 VA FATTO NEL TERMINALE PRIMA DI ESEGUIRE IL CODICE PYTHON 🚨
#   1) CREA FILE .env
#   2) DENTRO .env INSERISCI:
#       ADMIN_PASSWORD = (SCEGLI_PASSWORD)
#       DEBUG = True
#   3) $env:ADMIN_PASSWORD                                              🡸 PER VEDERE LA PASSWORD CHE HAI INSERITO
#   4) ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| HTTPS / NGNIX |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#    

#                    🚨 SERVE ESTENSIONE WLS (ubuntu) 🚨
#    /--------------------------------------------------------------------\
#   | sudo apt install nginx                            🡺 INSTALLA NGNIX  |
#   | sudo systemctl start nginx                        🡺 ATTIVA NGINX    |
#   | sudo systemctl stop nginx                         🡺 DISATTIVA NGINX |   COMANDI NGNIX
#   | sudo systemctl status nginx                       🡺 STATO NGINIX    |   WSL (ubuntu)
#   | sudo systemctl restart nginx                      🡺 RESTART NGNIX   |   
#   | sudo nginx -t                                     🡺 TEST NGNIX      |
#    \--------------------------------------------------------------------/

#               sudo nano /etc/nginx/sites-available/default
#--------------------------------------------------------------------- 🡸 SCRIPT BASH MODIFICATO
# server {
#    listen 443 ssl default_server;
#    listen [::]:443 ssl default_server; # type: ignore
#    server_name localhost;
#    ssl_certificate /etc/ssl/certs/selfsigned.crt;
#    ssl_certificate_key /etc/ssl/private/selfsigned.key;
#    location / {
#        proxy_pass http://127.0.0.1:8000;
#        proxy_set_header Host $host;
#        proxy_set_header X-Real-IP $remote_addr;
#        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#        proxy_set_header X-Forwarded-Proto $scheme;
#    }
# }
# server {
#   listen 80;
#    listen [::]:80;
#    server_name localhost;
#    location / {
#        return 301 https://$host$request_uri;
#    }
# }
#--------------------------------------------------------------------- 🡸 SCRIPT BASH MODIFICATO

# NGINX non riesce ad avviarsi perché il certificato SSL specificato non esiste 🡺 autogenerato per test locali
# Mostra un avviso nel browser ("connessione non sicura") perché non è firmato da una CA ufficiale                                                   

# 1) SOLO SE VUOI SALVARLI NEL PATH STANDART:
# sudo mkdir -p /etc/ssl/private

# 🚨 Keyout & out 🚨 SONO I PATH DI "server.key" e "server.ctr"
# SE LASCI VUOTO DOPO "\" 🡺 LI SALVA NELLA DIRECTORY CORRENTE
# 🚨 SE TOGLI "-nodes" 🚨 TOGLI LA PASSPHRASE
# 🚨 NON USARE LA PASSPHRASE SE USI --reload 🚨
# (UVICORN NON LA REINSERISCE AD OGNI AVVIO)

# 2) GENERA CERTIFICATO E CHIAVE (SENZA PASSPHRASE IN QUESTA DIRECTORY):
# sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
# -keyout server.key \
# -out server.crt \
# -subj "/C=IT/ST=Milano/L=Milano/O=Dev/OU=Localhost/CN=localhost"


# 🚨 PER AVVIARE 🚨
# python -m uvicorn BACKEND:app --host 127.0.0.1 --port 8000 --ssl-keyfile=server.key --ssl-certfile=server.crt

# SE FALLISCE, AGGIUNGI IL PATH:
# python -m uvicorn BACKEND:app --host 127.0.0.1 --port 8000 --ssl-keyfile="C:\Users\Sviatoslav\Desktop\ESAME APP\server.key" --ssl-certfile="C:\Users\Sviatoslav\Desktop\ESAME APP\server.crt"

#    /----------------------------------------------------------------------------------------\
#   | sudo lsof -i :80                                  🡺 VERIFICA CHI USA LA PORTA 80        |
#   | sudo lsof -i :3306                                🡺 VERIFICA CHI USA LA PORTA 3306      |   IN CASO DI 
#   | sudo kill {PID}                                   🡺 PID = PROCESSO DELLA LISTA DI SOPRA |   PROBLEMI
#   | sudo killall apache2                              🡺 AZZERA TUTTI I PROCESSI apache2     |   CON LE PORTE
#   | sudo killall mysqld                               🡺 AZZERA TUTTI I PROCESSI mysqld      |
#   | sudo killall nginx                                🡺 AZZERA TUTTI I PROCESSI nginx       |
#    \----------------------------------------------------------------------------------------/

#    /-------------------------------------------------------------------------\
#   | Let's Encrypt => gratuito e rinnovabile con un "certbot" ogni 90 giorni   |
#   | certbot renew --quiet                             🡺 COMANDO DI RINNOVO   |  SOLO DOMINI PUBBLICI
#   | sudo certbot renew --dry-run                      🡺 TEST RINNOVO         |
#    \-------------------------------------------------------------------------/

# 🚨"ngnix" E GLI EVENTUALI "mysql" / "apache2" INSTALLATI TRAMITE WSL(ubuntu) VANNO DISABILITATI PER EVITARE CONFLITTI CON MAMP 🚨

#    /-----------------------------------------------------------------------------\
#   |  sudo systemctl disable nginx                     🡺 DISABILITA NGNIX         |   DISABILITA SERVIZI
#   |  sudo systemctl disable mysql                     🡺 DISABILITA MYSQL (WSL)   |   WSL(ubuntu) PER EVITARE
#   |  sudo systemctl disable apache2                   🡺 DISABILITA NGNIX (WSL)   |   CONFLITTI CON MAMP
#    \-----------------------------------------------------------------------------/

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| LIMITE TENTATIVI LOGIN |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# pip install slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import PlainTextResponse
from fastapi import Query

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return PlainTextResponse("Too many requests", status_code=429)

#   @limiter.limit("5/minute")                                          🡸 MAX 5 LOGIN TENTATIVI AL MINUTO PER IP
#   async def login():
#       ...

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| GEOLOCALIZZAZIONE |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# pip install geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic                                 #   🡸 PER CALCOLARE DISTANZA TRA DUE PUNT   I
# pip install requests
import requests                                                     #   🡸 PER RICHIESTE HTTP A SITI ESTERNI

# DECODIFICATORE COORDINATE BINARY
import struct

# geolocator = Nominatim(user_agent="myapp")
# location = geolocator.geocode(indirizzo)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CONNESSIONE DATABASE |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# app = FastAPI()                                                   🡸 VEDI SEZIONE "LIMITE TENTATIVI LOGIN"
templates = Jinja2Templates(directory="templates")

# METODI HTTP -> GET, POST, HEAD, PUT, DELETE, PATCH, TRACE, OPTIONS, CONNECT
# PER "foo" SI INTENDE FUNZIONE

# "async" SIGNIFICA CHE NON ATTENDE LA FINE DI UN'ALTRA FUNZIONE, SE VUOLE PARTE ANCHE IN PARALLELO AL TUTTO

connessione = mysql.connector.connect(
    user = "Sviatoslav",     # STESSO UTENTE DI XAMP
    password = "",
    host = "localhost",
    port = "3306",           # LETTA DA MAMP
    database = "sviatoslav"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "https://localhost:4200"],  # Origini specifiche per credenziali
    allow_credentials=True,
    allow_methods=["*"],  # Permetti tutti i metodi HTTP (GET, POST, DELETE, ecc.)
    allow_headers=["*"],  # Permetti tutti gli header
)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| AVVIO |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# 🚨 NON USARE LA PASSPHRASE SE USI --reload 🚨
# (UVICORN NON LA REINSERISCE AD OGNI AVVIO)

#   C:\Users\Sviatoslav\Desktop\ESAME_APP

#   🡻 [⚠️SOLO HTTP⚠️] 🡻
#   python -m uvicorn BACKEND:app --reload

#   🡻 [⚠️HTTPS SENZA PASSPHRASE⚠️] 🡻
#   python -m uvicorn BACKEND:app --reload --host 127.0.0.1 --port 8000 --ssl-keyfile="server.key" --ssl-certfile="server.crt"
#   
#   🡻 [⚠️HTTPS CON SSL STESSA DIRECTORY DEL COMANDO⚠️] 🡻
#   python -m uvicorn BACKEND:app --host 127.0.0.1 --port 8000 --ssl-keyfile=server.key --ssl-certfile=server.crt

#   🡻 [⚠️HTTPS CON SSL DIRECTORY DIVERSA DAL COMANDO⚠️] 🡻
#   python -m uvicorn BACKEND:app --host 127.0.0.1 --port 8000 --ssl-keyfile="C:\Users\Sviatoslav\Desktop\ESAME APP\server.key" --ssl-certfile="C:\Users\Sviatoslav\Desktop\ESAME APP\server.crt"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| NAVIGAZIONE RAPIDA |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

#    🚨 USA IL FILE Genera Link.py PER SOSTITUIRE I LINK 🚨

# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L457    ━|CLASSI|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L485    ━|FUNZIONI|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L714    ━|SESSIONE|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L745    ━|LOGIN|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L833    ━|LOGOUT|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L846    ━|DETTAGLI UTENTE|━cd    
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L890    ━|FILTRO_UTENTI|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L985    ━|REGISTRAZIONE|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1144   ━|MODIFICA UTENTE|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1287   ━|ELIMINA UTENTE|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1349   ━|DETTAGLI ISCRIZIONE|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1392   ━|FILTRO ISCRIZIONI|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1507   ━|CREA ISCRIZIONE|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1621   ━|CANCELLA ISCRIZIONE|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1680   ━|CANCELLA ISCRIZIONI FILTRATE|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1778   ━|EVENTO SELEZIONATO|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1826   ━|CREA EVENTO|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L1996   ━|MODIFICA EVENTO|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L2161   ━|CANCELLA EVENTO|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L2205   ━|CANCELLA EVENTI FILTRATI|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L2285   ━|EVENTI FILTRATI|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L2528   ━|CATEGORIA SELEZIONATA|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L2559   ━|CREA CATEGORIA|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L2610   ━|MODIFICA CATEGORIA|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L2675   ━|CANCELLA CATEGORIA|━
# file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L2718   ━|CATEGORIE FILTRATE|━

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| LISTA CHIAMATE API |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# POST /LOGIN                                                                                               (1)   🡸   ---
# GET /LOGOUT                                                                                               (2)   🡸 LOGGATO

#                                         ❌ ━| UTENTE |━ ❌

# GET /ME                                                        "MIEI DATI & SESSIONE"                     (/)   🡸 LOGGATO
# GET /UTENTE                                                    "LISTA UTENTI"                                   🡸   ---
# GET /UTENTE/{ID_UTENTE}    [🤐COORDINATE,EMAIL,PASSWORD🤐]    "DATI ALTRI UTENTI"                              🡸   --- / ADMIN

# PUT /ME                                                        "MODIFICA MIEI DATI"                       (/)   🡸 LOGGATO
# PUT /UTENTE/ID_UTENTE}                                         "MODIFICA ALTRO UTENTE"                          🡸 ADMIN

# DELETE /ME                                                     "CANCELLA MIO ACCOUNT"                     (/)   🡸 LOGGATO
# DELETE /UTENTE/{ID_UTENTE}                                     "ELIMINA ALTRO UTENTE"                           🡸 ADMIN

#                                         ✅ ━| UTENTE |━ ✅

# GET /UTENTI/{ID_UTENTE}                                        "UTENTE SELEZIONATO"                       (3)   🡸 --- / ADMIN
# 🡹 [🤐COORDINATE,EMAIL,PASSWORD🤐] 🡹

# GET /UTENTI?ID_EVENTO=1&DATA=01-01-2026_31-01-2026&RICERCA=TESTO&ADMIN=1      "UTENTI FILTRATI"           (4)   🡸 --- / ADMIN
# 🡹 [🤐COORDINATE,EMAIL,PASSWORD🤐] 🡹

# POST /UTENTI                                                  "REGISTRAZIONE"                             (5)   🡸   ---

# PUT /UTENTI/{ID_UTENTE}                                       "MODIFICA UTENTE SELEZIONATO"               (6)   🡸 CREATORE / ADMIN
# 🡹 [⚠️ADMIN NON POSSONO MANOMETTERE ALTRI ADMIN⚠️] 🡹

# DELETE /UTENTI/{ID_UTENTE}                                    "CANCELLA UTENTE SELEZIONATO"               (7)   🡸 CREATORE / ADMIN
# 🡹 [⚠️ADMIN NON POSSONO MANOMETTERE ALTRI ADMIN⚠️] 🡹

# ℹ️ ID_EVENTO = {ID_EVENTO}
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)
# ℹ️ RICERCA = {...TESTO...}
# ℹ️ ADMIN = [0, 1]                                             (0 = NON ADMIN, 1 = ADMIN)

#                                         ❌ ━| ISCRIZIONI |━ ❌

# GET /TUTTI/{ID_EVENTO}/UTENTE                                  "TUTTI UTENTI EVENTO SELEZIONATO"          (/)    🡸 CREATORE / ADMIN
# GET /TUTTI/{ID_EVENTO}/UTENTE/{ID_UTENTE}                      "UTENTE ISCRITTO EVENTO SELEZIONATO"              🡸 CREATORE / ADMIN
# GET /CREATI/{ID_EVENTO}/UTENTE                                 "TUTTI UTENTI EVENTO ADMIN"                       🡸 CREATORE / ADMIN
# GET /CREATI/{ID_EVENTO}/UTENTE/{ID_UTENTE}                     "DATI UTENTE ISCRITTO EVENTO ADMIN"               🡸 ADMIN

# POST /TUTTI/{ID_EVENTO}/ISCRIZIONE/ME                          "MI ISCRIVO EVENTO SELEZIONATO"            (/)    🡸 LOGGATO
# POST /TUTTI/{ID_EVENTO}/ISCRIZIONE/{ID_UTENTE}                 "ISCRIVO ALTRO UTENTE EVENTO SELEZIONATO"         🡸 ADMIN
# POST /CREATI/{ID_EVENTO}/ISCRIZIONE/ME                         "MI ISCRIVO AL MIO EVENTO"                        🡸 CREATORE
# POST /CREATI/{ID_EVENTO}/ISCRIZIONE/{ID_UTENTE}                "ISCRIVO ALTRO UTENTE EVENTO ADMIN"               🡸 ADMIN

# DELETE /TUTTI/ISCRIZIONE/{PERIODO}                             "CANCELLA TUTTE ISCRIZIONI PERIODO"        (/)    🡸 CREATORE / ADMIN
# DELETE /TUTTI/ISCRIZIONE/ME                                    "CANCELLA TUTTE LE MIE ISCRIZIONI"                🡸 LOGGATO
# DELETE /TUTTI/{ID_EVENTO}/ISCRIZIONE/ME                        "CANCELLA MIA ISCRIZIONE EVENTO SELEZIONATO"      🡸 LOGGATO
# DELETE /TUTTI/{ID_EVENTO}/ISCRIZIONE                           "CANCELLA TUTTE ISCRIZIONI EVENTO SELEZIONATO"    🡸 CREATORE / ADMIN
# DELETE /TUTTI/{ID_EVENTO}/ISCRIZIONE/{ID_UTENTE}               "CANCELLA ISCRIZIONE UTENTE SELEZIONATO"          🡸 CREATORE / ADMIN
# DELETE /CREATI/{ID_EVENTO}/ISCRIZIONE                          "CANCELLA TUTTE ISCRIZIONI MIO EVENTO"            🡸 CREATORE
# DELETE /CREATI/{ID_EVENTO}/ISCRIZIONE/ME                       "CANCELLA MIA ISCRIZIONE MIO EVENTO"              🡸 CREATORE
# DELETE /CREATI/{ID_EVENTO}/{ID_UTENTE}                         "CANCELLA ISCRIZIONE ALTRUI EVENTO ADMIN"         🡸 CREATORE / ADMIN

#                                         ✅ ━| ISCRIZIONI UNIFICATE |━ ✅

# GET /ISCRIZIONI/{ID_EVENTO}/{ID_UTENTE}                        "DETTAGLI ISCRIZIONE SELEZIONATA"          (8)    🡸 ISCRITTO / CREATORE / ADMIN
# GET /ISCRIZIONI?TIPO=CREATI&ID_UTENTE=1&ID_EVENTO=1&DATA=01-01-2026_31-01-2026    "ISCRIZIONI FILTRATE"   (9)    🡸 LOGGATO

# POST /ISCRIZIONI/{ID_EVENTO}/{ID_UTENTE}                       "CREO ISCRIZIONE UTENTE-EVENTO"            (10)   🡸 CREATORE / ADMIN
# 🡹 [⚠️ADMIN NON POSSONO MANOMETTERE ALTRI ADMIN⚠️] 🡹         

# DELETE /ISCRIZIONI/{ID_EVENTO}/{ID_UTENTE}                     "ELIMINO ISCRIZIONE SELEZIONATA"           (11)   🡸 ISCRITTO / ADMIN
# DELETE /ISCRIZIONI?ID_UTENTE=1&ID_EVENTO=1&DATA=01-01-2026_31-01-2026  "ELIMINO ISCRIZIONE UTENTE-EVENTO" (12)   🡸 CREATORE / ADMIN
# 🡹 [⚠️ADMIN NON POSSONO MANOMETTERE ALTRI ADMIN⚠️] 🡹

# ℹ️ ID_EVENTO = {ID_EVENTO}
# ℹ️ ID_UTENTE = {ID_UTENTE}
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)

#                                         ❌ ━| EVENTI |━ ❌

# GET /TUTTI                                                     "VEDO TUTTI GLI EVENTI"                    (/)    🡸   ---
# GET /TUTTI/{ID_EVENTO}                                         "VEDO EVENTO SELEZIONATO"                         🡸   ---
# GET /CREATI/{ID_EVENTO}                                        "VEDO I MIEI EVENTI"                              🡸 LOGGATO / CREATORE                         
# GET /UTENTE/{ID_UTENTE}/CREATI/{ID_EVENTO}                     "EVENTI CREATI DA ALTRO UTENTE"                   🡸 ADMIN

# POST /TUTTI/                                                   "CREA MIO EVENTO"                          (/)    🡸 LOGGATO
# POST /CREATI/                                                                                                    🡸 LOGGATO
# POST /TUTTI/{ID_UTENTE}                                        "CREA EVENTO PER ALTRI UTENTI"                    🡸 ADMIN   

# PUT /TUTTI/{ID_EVENTO}                                         "MODIFICA EVENTO SELEZIONATO"              (/)    🡸 CREATORE / ADMIN
# PUT /CREATI/{ID_EVENTO}                                        "MODIFICA MIO EVENTO"                             🡸 CREATORE
# PUT /UTENTE/{ID_UTENTE}/CREATI/{ID_EVENTO}                     "MODIFICA EVENTO UTENTE SELEZIONATO"              🡸 ADMIN

# DELETE /TUTTI/{PERIODO}                                        "ELIMINA TUTTI EVENTI PERIODO"             (/)    🡸 CREATORE / ADMIN
# DELETE /TUTTI/{ID_EVENTO}                                      "ELIMINA MIO EVENTO"                              🡸 CREATORE
# DELETE /CREATI/{ID_EVENTO}                                                                                       🡸 LOGGATO / CREATORE
# DELETE /UTENTE/{ID_UTENTE}/CREATI/{ID_EVENTO}                  "ELIMINA EVENTO ALTRUI"                           🡸 ADMIN

#                                         ✅ ━| EVENTI UNIFICATI |━ ✅

# GET /EVENTI/{ID_EVENTO}                                        "EVENTO SELEZIONATO"                      (13)    🡸   ---

# POST /EVENTI/{ID_UTENTE}                                       "CREO EVENTO MIO O ALTRUI"                (14)    🡸 LOGGATO / ADMIN
# 🡹 [⚠️ADMIN NON POSSONO MANOMETTERE ALTRI ADMIN⚠️] 🡹

# PUT /EVENTI/{ID_EVENTO}                                        "MODIFICA EVENTO SELEZIONATO"             (15)    🡸 CREATORE / ADMIN

# DELETE /EVENTI/{ID_EVENTO}                                     "ELIMINA EVENTO SELEZIONATO"              (16)    🡸 CREATORE / ADMIN
# DELETE /EVENTI?ID_UTENTE=1&DATA=01-01-2026_31-01-2026          "ELIMINA EVENTI FILTRATI"                 (17)    🡸 CREATORE / ADMIN

# ℹ️ ID_EVENTO = {ID_EVENTO}
# ℹ️ ID_UTENTE = {ID_UTENTE}
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)

#                                         ❌ ━| FILTRI |━ ❌

# GET /TUTTI/SOLO_ISCRITTI                                       "TUTTI EVENTI A CUI SONO ISCRITTO"         (/)    🡸 LOGGATO
# GET /TUTTI/SOLO_ISCRITTI/{ID_EVENTO}                           "EVENTO A CUI SONO ISCRITTO"                      🡸 LOGGATO
# GET /CREATI/SOLO_ISCRITTI                                      "TUTTI EVENTI CREATI E ISCRITTO"                  🡸 CREATORE
# GET /CREATI/SOLO_ISCRITTI/{ID_EVENTO}                          "EVENTO CREATO E ISCRITTO"                        🡸 CREATORE
# GET /UTENTE/{ID_UTENTE}/SOLO_ISCRITTI                          "TUTTI EVENTI ISCRITTI UTENTE SELEZIONATO"        🡸 ADMIN
# GET /UTENTE/{ID_UTENTE}/SOLO_ISCRITTI/{ID_EVENTO}              "EVENTI ISCRITTI UTENTE SELEZIONATO"              🡸 ADMIN

# GET /TUTTI/SOLO_MAGGIORENNI                                    "TUTTI EVENTI SOLO MAGGIORENNI"            (/)    🡸 LOGGATO
# GET /TUTTI/SOLO_MAGGIORENNI/{ID_EVENTO}                        "EVENTO SOLO MAGGIORENNI"                         🡸 LOGGATO
# GET /CREATI/SOLO_MAGGIORENNI                                   "TUTTI EVENTI CREATI E SOLO MAGGIORENNI"          🡸 CREATORE
# GET /CREATI/SOLO_MAGGIORENNI/{ID_EVENTO}                       "EVENTO CREATO E SOLO MAGGIORENNI"                🡸 CREATORE
# GET /UTENTE/{ID_UTENTE}/SOLO_MAGGIORENNI                       "EVENTI SOLO MAGGIORENNI PER UTENTE"              🡸 ADMIN
# GET /UTENTE/{ID_UTENTE}/SOLO_MAGGIORENNI/{ID_EVENTO}           "EVENTI SOLO MAGGIORENNI UTENTE SELEZIONATO"      🡸 ADMIN

# GET /TUTTI/PER_DATA                                            "TUTTI EVENTI PER DATA"                    (/)    🡸 LOGGATO
# GET /TUTTI/PER_DATA/{ID_EVENTO}                                "EVENTO SELEZIONATO PER DATA"                     🡸 LOGGATO
# GET /CREATI/PER_DATA                                           "TUTTI EVENTI CREATI E PER DATA"                  🡸 CREATORE
# GET /CREATI/PER_DATA/{ID_EVENTO}                               "EVENTO CREATO E PER DATA"                        🡸 CREATORE
# GET /UTENTE/{ID_UTENTE}/PER_DATA                               "TUTTI EVENTI PER DATA UTENTE SELEZIONATO"        🡸 ADMIN
# GET /UTENTE/{ID_UTENTE}/PER_DATA/{ID_EVENTO}                   "EVENTI PER DATA UTENTE SELEZIONATO"              🡸 ADMIN

# GET /TUTTI/PER_ALFABETO                                        "TUTTI EVENTI PER ALFABETO"                (/)    🡸 LOGGATO
# GET /TUTTI/PER_ALFABETO/{ID_EVENTO}                            "EVENTO SELEZIONATO PER ALFABETO"                 🡸 LOGGATO
# GET /CREATI/PER_ALFABETO                                       "TUTTI EVENTI CREATI E PER ALFABETO"              🡸 CREATORE
# GET /CREATI/PER_ALFABETO/{ID_EVENTO}                           "EVENTO CREATO E PER ALFABETO"                    🡸 CREATORE
# GET /UTENTE/{ID_UTENTE}/PER_ALFABETO                           "TUTTI EVENTI PER ALFABETO UTENTE SELEZIONATO"    🡸 ADMIN
# GET /UTENTE/{ID_UTENTE}/PER_ALFABETO/{ID_EVENTO}               "EVENTI PER ALFABETO UTENTE SELEZIONATO"          🡸 ADMIN

# GET /TUTTI/PER_PREZZO                                          "TUTTI EVENTI PER PREZZO"                  (/)    🡸 LOGGATO
# GET /TUTTI/PER_PREZZO/{ID_EVENTO}                              "EVENTO SELEZIONATO PER PREZZO"                   🡸 LOGGATO
# GET /CREATI/PER_PREZZO                                         "TUTTI EVENTI CREATI E PER PREZZO"                🡸 CREATORE
# GET /CREATI/PER_PREZZO/{ID_EVENTO}                             "EVENTO CREATO E PER PREZZO"                      🡸 CREATORE
# GET /UTENTE/{ID_UTENTE}/PER_PREZZO                             "TUTTI EVENTI PER PREZZO UTENTE SELEZIONATO"      🡸 ADMIN
# GET /UTENTE/{ID_UTENTE}/PER_PREZZO/{ID_EVENTO}                 "EVENTI PER PREZZO UTENTE SELEZIONATO"            🡸 ADMIN

# GET /TUTTI/PER_CATEGORIA                                       "TUTTI EVENTI PER CATEGORIA"               (/)    🡸 LOGGATO
# GET /TUTTI/PER_CATEGORIA/{ID_EVENTO}                           "EVENTO SELEZIONATO PER CATEGORIA"                🡸 LOGGATO
# GET /CREATI/PER_CATEGORIA                                      "TUTTI EVENTI CREATI E PER CATEGORIA"             🡸 CREATORE
# GET /CREATI/PER_CATEGORIA/{ID_EVENTO}                          "EVENTO CREATO E PER CATEGORIA"                   🡸 CREATORE
# GET /UTENTE/{ID_UTENTE}/PER_CATEGORIA                          "TUTTI EVENTI PER CATEGORIA UTENTE SELEZIONATO"   🡸 ADMIN
# GET /UTENTE/{ID_UTENTE}/PER_CATEGORIA/{ID_EVENTO}              "EVENTI PER CATEGORIA UTENTE SELEZIONATO"         🡸 ADMIN            

# GET /TUTTI/PER_DISTANZA                                        "TUTTI EVENTI PER DISTANZA"                (/)    🡸 LOGGATO
# GET /TUTTI/PER_DISTANZA/{ID_EVENTO}                            "EVENTO SELEZIONATO PER DISTANZA"                 🡸 LOGGATO
# GET /CREATI/PER_DISTANZA                                       "TUTTI EVENTI CREATI E PER DISTANZA"              🡸 CREATORE
# GET /CREATI/PER_DISTANZA/{ID_EVENTO}                           "EVENTO CREATO E PER DISTANZA"                    🡸 CREATORE
# GET /UTENTE/{ID_UTENTE}/PER_DISTANZA                           "TUTTI EVENTI PER DISTANZA UTENTE SELEZIONATO"    🡸 ADMIN
# GET /UTENTE/{ID_UTENTE}/PER_DISTANZA/{ID_EVENTO}               "EVENTI PER DISTANZA UTENTE SELEZIONATO"          🡸 ADMIN     

#                                         ✅ ━| FILTRI UNIFICATI |━ ✅    

# GET /EVENTI?TIPO=TUTTI&                                        "FILTRO EVENTI"                            (17)   🡸   ---
# ID_UTENTE=1&
# ISCRITTO=True&
# MAGGIORENNI=True&
# DATA=01-01-2026_31-01-2026&
# PER_ALFABETO=>&
# PREZZO=10_50&
# CATEGORIA=CONCERTO&
# DISTANZA=1_50&
# RICERCA=PIZZA

# ℹ️ ID_UTENTE = {ID_UTENTE}                                                                                        
# ℹ️ TIPO = [CREATI, TUTTI]
# ℹ️ ISCRITTO = [True, False]
# ℹ️ MAGGIORENNI = [True, False]
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)
# ℹ️ ALFABETO = [<, >]
# ℹ️ PREZZO = [<{PREZZO}, >{PREZZO}, {PREZZO}]
# ℹ️ CATEGORIA = [CONCERTO, ARTE, SPORT, CIBO, CINEMA, CERIMONIA, INTRATTENIMENTO, FORMAZIONE, MOSTRA]
# ℹ️ DISTANZA = [<{INSERIMENTO(Km)}, >{INSERIMENTO(Km)}, {INSERIMENTO(Km)}]
# ℹ️ RICERCA = {...TESTO...}

#                                         ✅ ━| CATEGORIE |━ ✅   

# GET /CATEGORIE/{ID_CATEGORIA}                                 "CATEGORIA SELEZIONATA"                   (18)   🡸   ---
# POST /CATEGORIE                                               "CREA CATEGORIA"                          (19)   🡸 ADMIN
# PUT /CATEGORIE/{ID_CATEGORIA}                                 "MODIFICA CATEGORIA SELEZIONATA"          (20)   🡸 ADMIN
# DELETE /CATEGORIE/{ID_CATEGORIA}                              "ELIMINA CATEGORIA SELEZIONATA"           (21)   🡸 ADMIN

# GET /CATEGORIE?RICERCA=TESTO&ID_UTENTE=1                      "CATEGORIE FILTRATE"                      (22)   🡸   ---
# ℹ️ ID_UTENTE = {ID_UTENTE}
# 🡹 [⚠️SOLO ADMIN POSSONO FILTRARE PER UTENTE⚠️] 🡹
# ℹ️ RICERCA = {...TESTO...}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CLASSI |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# AGGIORNAMENTO PARZIALE UTENTE (PUT)
class UtenteUpdate(BaseModel):
    ID_UTENTE: Optional[int] = None
    EMAIL_UTENTE: Optional[str] = None
    PASSWORD_UTENTE: Optional[str] = None
    NOME_UTENTE: Optional[str] = None
    DATA_REGISTRAZIONE: Optional[str] = None  # oppure datetime
    CHECK_ADMIN: Optional[bool] = None
    COORDINATE_UTENTE: Optional[str] = None  # es: "POINT(12.34 56.78)"
    INDIRIZZO_UTENTE: Optional[str] = None

# AGGIORNAMENTO PARZIALE EVENTO (PUT)
class EventoUpdate(BaseModel):
    ID_EVENTO: Optional[int] = None
    NOME_EVENTO: Optional[str] = None
    DESCRIZIONE_EVENTO: Optional[str] = None
    DATA_EVENTO: Optional[str] = None  # oppure datetime
    COSTO: Optional[float] = None
    MAX_PARTECIPANTI: Optional[int] = None
    CHECK_MAGGIORENNI: Optional[bool] = None
    COORDINATE_EVENTO: Optional[str] = None  # es: "POINT(12.34 56.78)"
    INDIRIZZO_EVENTO: Optional[str] = None
    PASSWORD_EVENTO: Optional[str] = None

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| FUNZIONI |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

def conversione(result): #   🡸 USA UNA LISTA DI VALORI (result) E NON UNA SINGOLA RIGA (result[0]) 
    for row in result:
        for key in list(row.keys()):                                #   🡸 CREA COPIA DELLE CHIAVI
            value = row[key]                                        #   🡸 row[key] È LA RISPOSTA AL JSON
            if isinstance(value, (date, datetime)):
                row[key] = value.isoformat()                        #   🡸 CONVERSIONE STRINGA ISO 8601
            elif isinstance(value, Decimal):
                row[key] = float(value)                             #   🡸 (DECIMAL => FLOAT)  
            elif isinstance(value, bytes):
                try:
                    row[key] = value.decode('utf-8')                #   🡸 PROVA DECODIFICARE COME UTF-8
                except UnicodeDecodeError:
                    row[key] = value.hex()                          #   🡸 CONVERSIONE IN STRINGA ESADECIMALE COME FALLBACK
            elif isinstance(value, str) and value.startswith("POINT("):
                # ESTRAZIONE COORDINATE DA STRINGA "POINT(x y)"
                coords = value[6:-1].split()
                longitudine = float(coords[0])
                latitudine = float(coords[1])
                # SALVA COMPATIBILE CON SRID
                row[key] = f"{latitudine} {longitudine}"
    return result

# CONVERSIONE STRINGA IN COORDINATE SRID=4326;POINT(LON LAT)
def normalizza_coordinate_input(coordinate_str: str) -> str:
    coordinate_str = coordinate_str.strip()
    # Se già in formato POINT(lon lat)
    if coordinate_str.startswith("POINT(") and coordinate_str.endswith(")"):
        coords = coordinate_str[6:-1].split()
        if len(coords) == 2:
            lon, lat = map(float, coords)
            return f"POINT({lon} {lat})"
        else:
            raise ValueError("Formato POINT non valido")
    # Se formato "lat lon"
    else:
        lat, lon = map(float, coordinate_str.split())
        return f"POINT({lon} {lat})"

# REVERSE GEOCODING
def indirizzo_da_coordinate(coordinate: str):
    geolocator = Nominatim(user_agent="myapp")
    punto = coordinate.strip().replace("POINT(", "").replace(")", "")
    longitudine, latitudine= map(float, punto.split())
    location = geolocator.reverse((latitudine, longitudine))
    if location is None:
        raise ValueError("Coordinate non valide o non trovate")
    return location.address

# VERIFICA DISTANZA COORDINATE E INDIRIZZO
def verifica_coordinate_indirizzo(indirizzo: str, coordinate: str = None, soglia_metri: float = 100.0):
    geolocator = Nominatim(user_agent="myapp")
    location = geolocator.geocode(indirizzo, timeout=10)
    # SE NON TROVATO
    if location is None:
        raise ValueError("Indirizzo non valido o non trovato")
    longitudine_nominatim, latitudine_nominatim = location.longitude, location.latitude
    coordinate_nominatim = (latitudine_nominatim, longitudine_nominatim)
    # SE NON FORNITE COORDINATE 🡺 COORDINATE NOMINATIM
    if not coordinate:
        logging.info("Coordinate non fornite, usando quelle di Nominatim")
        return {
            "coordinate": f"{latitudine_nominatim} {longitudine_nominatim}",  # senza POINT
            "distanza_metri": 0
        }
    # SE FORNITE COORDINATE 🡺 CONVERTITE IN TUPLA
    try:
        lat_str, lon_str = coordinate.strip().split()
        lat_utente = float(lat_str)
        lon_utente = float(lon_str)
        coordinate_utente = (lat_utente, lon_utente)
    # SE NON VALIDO
    except Exception:
        raise ValueError("Formato COORDINATE_UTENTE non valido. Usa 'lat lon' come stringa.")
    # CALCOLO DISTANZA
    distanza = geodesic(coordinate_nominatim, coordinate_utente).meters
    # SE DISTANZA MAGGIORE DELLA SOGLIA
    if distanza > soglia_metri:
        raise ValueError(f"Coordinate non coerenti con l'indirizzo. Distanza: {distanza:.2f} metri")
    # RISPOSTA JSON
    return {
        "coordinate": f"{lat_utente} {lon_utente}",  # senza POINT, solo lat lon
        "distanza_metri": round(distanza, 2)
    }

def verifica_admin(id_sessione: int, cursor):
    # SE NON LOGGATO 🡺 FALSE
    if not id_sessione:
        return None, False
    # QUERY VERIFICA ADMIN
    query = "SELECT CHECK_ADMIN FROM utente WHERE ID_UTENTE = %s"
    cursor.execute(query, (id_sessione,))
    result = cursor.fetchone()
    # SE TROVATO E ADMIN 🡺 TRUE
    if result and result.get("CHECK_ADMIN") == 1:
        return id_sessione, True
    # SE TROVATO O NON ADMIN 🡺 FALSE
    else:
        return id_sessione, False

# QUERY DATI UTENTE (UNIFICATA)
def query_utente(id_utente: int, cursor, full_data: bool = True):
    if full_data:
        query = """
            SELECT ID_UTENTE, EMAIL_UTENTE, NOME_UTENTE, DATA_REGISTRAZIONE, CHECK_ADMIN, INDIRIZZO_UTENTE,
                   ST_AsText(COORDINATE_UTENTE) AS COORDINATE_UTENTE
            FROM utente
            WHERE ID_UTENTE = %s
        """
    else:
        query = """
            SELECT ID_UTENTE, NOME_UTENTE, DATA_REGISTRAZIONE, CHECK_ADMIN
            FROM utente
            WHERE ID_UTENTE = %s
        """
    cursor.execute(query, (id_utente,))
    return cursor.fetchone()

# FILTRO DATA DINAMICO
def genera_filtro_data(data_filter: str, nome_colonna_sql: str):
    condizioni = []
    valori = []
    # SE NESSUN FILTRO
    if not data_filter:
        return condizioni, valori
    data_filter = data_filter.strip()
    # INTERVALLO: 01-01-2025_31-01-2025
    if "_" in data_filter:
        parts = data_filter.split("_")
        if len(parts) != 2:
            raise HTTPException(status_code=400, detail="Intervallo data non valido: usare 'DD-MM-YYYY_DD-MM-YYYY'")
        data_1_str, data_2_str = parts[0].strip(), parts[1].strip()
        try:
            data_1 = datetime.strptime(data_1_str, "%d-%m-%Y").date()
            data_2 = datetime.strptime(data_2_str, "%d-%m-%Y").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato data nell'intervallo non valido: usare DD-MM-YYYY")
        condizioni.append(f"DATE({nome_colonna_sql}) BETWEEN %s AND %s")
        valori.extend([data_1, data_2])
        return condizioni, valori
    # SINGOLA DATA CON OPERATORE SIMBOLICO: >01-01-2025, <=31-12-2025
    simbolo_match = re.match(r"^(<=|>=|<|>)\s*(\d{2}-\d{2}-\d{4})$", data_filter)
    if simbolo_match:
        oper, data_str = simbolo_match.groups()
        try:
            data_obj = datetime.strptime(data_str, "%d-%m-%Y").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato data non valido: usare DD-MM-YYYY")
        # Valida operatore con whitelist
        cond = build_sql_condition(f"DATE({nome_colonna_sql})", oper, "COMPARAZIONE")
        condizioni.append(cond)
        valori.append(data_obj)
        return condizioni, valori
    plain_date = re.match(r"^(\d{2}-\d{2}-\d{4})$", data_filter)
    if plain_date:
        try:
            data_obj = datetime.strptime(plain_date.group(1), "%d-%m-%Y").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato data non valido: usare DD-MM-YYYY")
        condizioni.append(f"DATE({nome_colonna_sql}) = %s")
        valori.append(data_obj)
        return condizioni, valori
    # ERRORE FORMATO
    raise HTTPException(
        status_code=400,
        detail="Formato data non valido: usare operatori simbolici (> < >= <=) oppure un intervallo con '_' (es. 01-01-2025_31-01-2025)"
    )

# OPERATORI SQL CONSENTITI PER FILTRI DINAMICI
ALLOWED_SQL_OPERATORS = {
    "COMPARAZIONE": ["<", ">", "<=", ">=", "="],
    "ALFABETO": ["<", ">"],
}

# COSTRUISCE CONDIZIONE SQL CON OPERATORE VALIDATO
def build_sql_condition(colonna: str, operatore: str, tipo: str) -> str:
    allowed = ALLOWED_SQL_OPERATORS.get(tipo, [])
    if operatore.strip() not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Operatore '{operatore}' non consentito per {tipo}. "
                   f"Usa: {', '.join(allowed)}"
        )
    return f"{colonna} {operatore.strip()} %s"

# NORMALIZZAZIONE INPUT

# NORMALIZZAZIONE UNIFICATA INPUT (stringa, booleano, numero)
def normalizza_input_nullo(value, tipo="str"):
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.lower() in ("null", "none", "undefined"):
        return None
    if tipo == "bool":
        if isinstance(value, bool):
            return value
        if s in ("1", "true", "yes", "on"):
            return True
        if s in ("0", "false", "no", "off"):
            return False
        return None
    if tipo == "num":
        try:
            return float(s) if "." in s else int(s)
        except ValueError:
            return None
    return s

# QUERY DATI CATEGORIA
def query_categoria(id_categoria: int, cursor, full_data: bool = False):
    if full_data:
        query = """
            SELECT ID_CATEGORIA, NOME_CATEGORIA, ID_UTENTE
            FROM categoria
            WHERE ID_CATEGORIA = %s
        """
    else:
        query = """
            SELECT ID_CATEGORIA, NOME_CATEGORIA
            FROM categoria
            WHERE ID_CATEGORIA = %s
        """
    cursor.execute(query, (id_categoria,))
    return cursor.fetchone()

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| SESSIONE (0) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /ME
@app.get("/ME")
async def utente_me(request: Request):

    # VERIFICA SESSIONE
    id_utente = request.session.get("ID_UTENTE")
    if not id_utente:
        raise HTTPException(status_code=401, detail="Non sei loggato") 

    # INIZIO  
    with connessione.cursor(dictionary=True) as cursor:
        # VISUALIZZA UTENTE (NO PASSWORD)       
        result = query_utente(id_utente, cursor, full_data=True)

        # È VUOTO ?
        if not result:
            raise HTTPException(status_code=404, detail="Utente non trovato")
        
        # CONVERSIONE TIMESTAMP E COORDINATE
        result_convertito = conversione([result])[0] 

        # RISPOSTA JSON
        return JSONResponse({
            "message": "Sei loggato",
            "utente": result_convertito
        })

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| LOGIN (1) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# CONFIGURAZIONE LOGGING
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# CONFIGURAZIONE SESSIONE
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
if SECRET_KEY == "dev-secret-change-me":
    logging.warning("Using default SECRET_KEY — impostare SECRET_KEY nel file .env o come variabile d'ambiente in produzione")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# POST /LOGIN
@limiter.limit("5/minute")                                          #   🡸 MAX 5 LOGIN TENTATIVI AL MINUTO PER IP
@app.post("/LOGIN")
async def login(request: Request):
    logging.info("Login attempt")

    # STRUTTURA JSON
    data = await request.json()
    email = normalizza_input_nullo(data.get("EMAIL_UTENTE"), tipo="str")
    password = normalizza_input_nullo(data.get("PASSWORD_UTENTE"), tipo="str")

    # INIZIO 
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # UTENTE ESISTE ? (verifica solo l'email)
            query = "SELECT * FROM utente WHERE EMAIL_UTENTE = %s"
            dati = (email,)
            cursor.execute(query, dati)
            result = cursor.fetchone()

            # SE NON ESISTE
            if not result:
                logging.warning("Login failed: user not found email=%s", email)
                return JSONResponse({"message": "Credenziali non valide"}, status_code=401)

            # SE ESISTE
            hashed_password = result["PASSWORD_UTENTE"]  # La password nel database è già hashata
        
            # CONFRONTO HASH PASSWORD INSERITA CON HASH PASSWORD DATABASE
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # PASSWORD CORRETTA
                id_sessione = result["ID_UTENTE"]

                # SALVA COORDINATE UTENTE NELLA SESSIONE (se presenti)
                coordinate_db = result.get("COORDINATE_UTENTE")

                # SALVA COORDINATE UTENTE NELLA SESSIONE TODO
                if coordinate_db and isinstance(coordinate_db, bytes):
                    try:
                        srid = struct.unpack("<I", coordinate_db[:4])[0]  # facoltativo
                        x, y = struct.unpack("<dd", coordinate_db[9:])     # 2 double: lon, lat
                        # Salva come "lat lon" (stringa compatibile con filtro distanza)
                        coordinate_latlon = f"{y} {x}"
                        request.session["COORDINATE"] = coordinate_latlon
                        logging.info("Coordinate utente salvate in sessione")
                    except struct.error as se:
                        logging.exception("Error parsing binary coordinate data")
                        request.session["COORDINATE"] = None
                    except Exception as e:
                        logging.exception("Unexpected error converting coordinates")
                        request.session["COORDINATE"] = None

                # ACCESSO ESEGUITO - Salva nella sessione
                request.session["ID_UTENTE"] = id_sessione
                logging.info("Accesso consentito, sessione impostata: %s", id_sessione)

                # VISUALIZZA UTENTE
                result = query_utente(id_sessione, cursor, full_data=True)

                # CONVERSIONE TIMESTAMP E COORDINATE
                result_convertito = conversione([result])[0] 
                return JSONResponse({
                    "message": "Login effettuato con successo",
                    "utente": result_convertito
                })
            else:
                # PASSWORD ERRATA
                logging.warning("Login failed: wrong password for email=%s", email)
                return JSONResponse({"message": "Credenziali non valide"}, status_code=401)
        
    # ERRORE NELLA QUERY
    except mysql.connector.Error:
        logging.exception("Errore DB durante login")
        return JSONResponse({"message": "Errore interno"}, status_code=500)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| LOGOUT (2) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /LOGOUT
@app.get("/LOGOUT")
async def logout(request: Request):
    # Cancella la sessione se esiste
    if "ID_UTENTE" in request.session:
        request.session.clear()
    return JSONResponse({"message": "Logout effettuato con successo"})

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| DETTAGLI UTENTE (3) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /UTENTI/{ID_UTENTE}
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹

# ADMIN PUÒ VEDERE TUTTI I DETTAGLI [MAIL, COORDINATE] MA NON [PASSOWRD]
# UTENTE ESTERNO VEDE SOLO [ID_UTENTE, DATA_REGISTRAZIONE, CHECK_ADMIN]

@app.get("/UTENTI/{ID_UTENTE}")
async def get_utente(ID_UTENTE: int, request: Request):

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA SESSIONE
            id_sessione = request.session.get("ID_UTENTE")

            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # SE È IL PROPRIO PROFILO O ADMIN
            is_full_data = (id_verificato == ID_UTENTE or is_admin)
            result = query_utente(ID_UTENTE, cursor, full_data=is_full_data)

            # SE NON TROVATO
            if not result:
                raise HTTPException(status_code=404, detail=f"Nessun utente con ID {ID_UTENTE} trovato")

            # CONVERSIONE
            result_convertito = conversione([result])[0]

            # RISPOSTA JSON
            return JSONResponse({
                "message": f"Dettagli utente {ID_UTENTE} trovati",
                "utente": result_convertito
            })

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error retrieving user details")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| FILTRO UTENTI (4) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /UTENTI?ID_EVENTO=1&DATA=01-01-2026_31-01-2026&RICERCA=TESTO&ADMIN=1
# ℹ️ ID_EVENTO = {ID_EVENTO}
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)
# ℹ️ RICERCA = {...TESTO...}
# ℹ️ ADMIN = [0, 1]                                             (0 = NON ADMIN, 1 = ADMIN)
@app.get("/UTENTI")
async def get_utenti(request: Request):

    # PARAMETRI FILTRO
    params = request.query_params
    id_evento = normalizza_input_nullo(params.get("ID_EVENTO"), tipo="str")
    data_filter = normalizza_input_nullo(params.get("DATA"), tipo="str")
    ricerca = normalizza_input_nullo(params.get("RICERCA"), tipo="str")
    admin = normalizza_input_nullo(params.get("ADMIN"), tipo="bool")

    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # SOLO ADMIN VEDE DATI COMPLETI (EMAIL, COORDINATE, INDIRIZZO)
            if is_admin:
                # QUERY BASE ALL (ADMIN)
                query = """
                    SELECT utente.ID_UTENTE, EMAIL_UTENTE, NOME_UTENTE, CHECK_ADMIN, DATA_REGISTRAZIONE,
                    INDIRIZZO_UTENTE, ST_AsText(COORDINATE_UTENTE) AS COORDINATE_UTENTE
                    FROM utente
                """
            else:
                # QUERY BASE PART (UTENTE NORMALE)
                query = """
                    SELECT utente.ID_UTENTE, NOME_UTENTE, CHECK_ADMIN, DATA_REGISTRAZIONE
                    FROM utente
                """
            conditions = []
            values = []

            # FILTRO ID_EVENTO
            if id_evento:
                query += " JOIN evento ON utente.ID_UTENTE = evento.ID_UTENTE"
                conditions.append("evento.ID_EVENTO = %s")
                values.append(id_evento)

            # FILTRO DATA
            try:
                condizioni_data, valori_data = genera_filtro_data(data_filter, "DATA_REGISTRAZIONE")
                conditions.extend(condizioni_data)
                values.extend(valori_data)
                
            # ERRORE DATA
            except HTTPException as e:
                return JSONResponse(content={"errore": e.detail}, status_code=e.status_code)

            # FILTRO RICERCA (LIKE)
            if ricerca:
                conditions.append("LOWER(NOME_UTENTE) LIKE %s")
                values.append(f"%{ricerca.lower()}%")

            # FILTRO ADMIN (0 / 1)
            if admin == "1":
                conditions.append("CHECK_ADMIN = 1")
            elif admin == "0":
                conditions.append("CHECK_ADMIN = 0")

            # COSTRUZIONE WHERE DINAMICA
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            # ORDINO PER DATA ED ESEGUO QUERY
            query += " ORDER BY DATA_REGISTRAZIONE DESC"
            cursor.execute(query, tuple(values))
            utenti = cursor.fetchall()

            # CONVERSIONE TIMESTAMP E COORDINATE
            utenti_convertiti = conversione(utenti)

            # RISPOSTA JSON
            return JSONResponse(content={"utenti": utenti_convertiti})

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error retrieving users")
        raise HTTPException(status_code=500, detail="Errore database durante il recupero utenti")
    except Exception as e:
        logging.exception("Unexpected error retrieving users")
        raise HTTPException(status_code=500, detail="Errore interno inatteso")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| REGISTRAZIONE (5) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# POST /UTENTI
@app.post("/UTENTI")
async def register(request: Request):
    logging.info("Registration attempt")
    EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    # STRUTTURA JSON
    data = await request.json()
    email = normalizza_input_nullo(data.get("EMAIL_UTENTE"), tipo="str")
    password = normalizza_input_nullo(data.get("PASSWORD_UTENTE"), tipo="str")
    nome = normalizza_input_nullo(data.get("NOME_UTENTE"), tipo="str")
    coordinate = normalizza_input_nullo(data.get("COORDINATE_UTENTE"), tipo="str")  # "latitudine longitudine"
    indirizzo = normalizza_input_nullo(data.get("INDIRIZZO_UTENTE"), tipo="str")  # "Via Roma, Milano"
    richiesta_admin = int(data.get("CHECK_ADMIN", 0))
    admin_password_fornita = normalizza_input_nullo(data.get("ADMIN_PASSWORD", None), tipo="str")

    # VERIFICA SESSIONE
    if not nome or not nome.strip():
        return JSONResponse({"message": "Nome utente obbligatorio"}, status_code=422)

    # SE NON LOGGATO
    if not email or not EMAIL_REGEX.match(email):
        return JSONResponse({"message": "Email non valida"}, status_code=422)

    # VERIFICA ADMIN
    try:
        check_admin = 0
        if richiesta_admin == 1:
            password_admin_corretta = os.getenv("ADMIN_PASSWORD")
            if not password_admin_corretta:
                raise RuntimeError("ADMIN_PASSWORD non definita nel file .env")
            if admin_password_fornita != password_admin_corretta:
                raise PermissionError("Password amministratore non valida")
            check_admin = 1
    except PermissionError as e:
        logging.warning("Admin password validation failed")
        return JSONResponse({"message": "Credenziali amministratore non valide"}, status_code=403)
    except (TypeError, ValueError) as ve:
        logging.exception("Invalid admin verification parameters")
        return JSONResponse({"message": "Errore nella verifica amministratore"}, status_code=400)
    except Exception as e:
        logging.exception("Unexpected error during admin verification")
        return JSONResponse({"message": "Errore interno verifica admin"}, status_code=500)

    # SE SOLO COORDINATE 
    if not indirizzo and coordinate:
        logging.info("Coordinate provided without address, looking up address")
        indirizzo = indirizzo_da_coordinate(normalizza_coordinate_input(coordinate))

    # SE SOLO INDIRIZZO
    coordinate_raw = coordinate
    coordinate_db = None
    if coordinate:
        try:
            logging.info("Processing coordinate input")
            # CONVERTI COORDINATE IN "POINT(lon lat)"
            coordinate_db = normalizza_coordinate_input(coordinate)

        # ERRORE DI CONVERSIONE
        except ValueError as ve:
            return JSONResponse({"message": str(ve)}, status_code=422)

    # SE INDIRRIZZO
    try:
        if indirizzo:
            risultato_verifica = verifica_coordinate_indirizzo(indirizzo, coordinate_raw)
            distanza = risultato_verifica["distanza_metri"]

            # CONVERTI COORDINATE IN "POINT(lon lat)"
            coordinate_db = normalizza_coordinate_input(risultato_verifica["coordinate"])

        # SE COORDINATE NON VALIDE
        else:
            return JSONResponse({"message": "È necessario fornire COORDINATE_UTENTE o INDIRIZZO_UTENTE"}, status_code=400)

    # ERRORE DI GEOCODIFICA
    except ValueError as ve:
        logging.exception("Geocoding validation error")
        return JSONResponse({"message": str(ve)}, status_code=400)
    except Exception as e:
        logging.exception("Unexpected error during geocoding")
        return JSONResponse({"message": "Errore interno durante la geocodifica"}, status_code=500)

    # SE COORDINATE NON VALIDE
    if not coordinate_db:
        return JSONResponse({"message": "Coordinate utente mancanti o non valide"}, status_code=422)

    # HASH PASSWORD
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        columns = ["EMAIL_UTENTE", "PASSWORD_UTENTE", "NOME_UTENTE", "CHECK_ADMIN"]
        placeholders = ["%s", "%s", "%s", "%s"]
        values = [email, hashed_password, nome, check_admin]

        # AGGIUNTA COORDINATE
        if coordinate_db:
            columns.append("COORDINATE_UTENTE")
            placeholders.append("ST_GeomFromText(%s, 4326)")
            values.append(coordinate_db)

        # AGGIUNTA INDIRIZZO
        if indirizzo:
            columns.append("INDIRIZZO_UTENTE")
            placeholders.append("%s")
            values.append(indirizzo)

        # VERIFICA EMAIL ESISTENTE
        with connessione.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM utente WHERE EMAIL_UTENTE = %s", (email,))
            result = cursor.fetchone()

            # SE EMAIL ESISTE
            if result:
                return JSONResponse({"message": "Email già registrata"}, status_code=400)

        # QUERY DI INSERIMENTO
        query = f"""
            INSERT INTO utente ({', '.join(columns)}) 
            VALUES ({', '.join(placeholders)})
        """
        logging.info("Inserting new user with coordinates")

        # ESECUZIONE QUERY
        with connessione.cursor(dictionary=True) as cursor:
            cursor.execute(query, tuple(values))
            connessione.commit()
            id_utente = cursor.lastrowid

        # VISUALIZZA UTENTE (NO PASSWORD)
        with connessione.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT ID_UTENTE, EMAIL_UTENTE, NOME_UTENTE, CHECK_ADMIN, DATA_REGISTRAZIONE, INDIRIZZO_UTENTE,
                ST_AsText(COORDINATE_UTENTE) AS COORDINATE_UTENTE
                FROM utente
                WHERE ID_UTENTE = %s
            """, (id_utente,))
            nuovo_utente = cursor.fetchone()

        # CONVERSIONE TIMESTAMP E COORDINATE
        utente_convertito = conversione([nuovo_utente])[0]
        logging.info("User registered successfully")

        # RISPOSTA JSON
        return JSONResponse({
            "message": "Registrazione avvenuta con successo",
            "utente": utente_convertito,
            "distanza_coordinate_indirizzo": distanza
        })

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error during user registration")
        return JSONResponse({"message": "Errore interno"}, status_code=500)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| MODIFICA UTENTE (6) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# PUT /UTENTI/{ID_UTENTE}
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹
@app.put("/UTENTI/{ID_UTENTE}")
async def update_utente(ID_UTENTE: int, request: Request):
    cursor = None
    distanza = None

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA SESSIONE
            id_sessione = request.session.get("ID_UTENTE")

            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # INPUT JSON
            data = await request.json()
            utente_update = UtenteUpdate(**data)

            # SE NON ADMIN E NON PROPRIO PROFILO
            if not is_admin and id_verificato != ID_UTENTE:
                raise HTTPException(status_code=403, detail="Non hai i permessi per modificare questo utente")
            
            # SE NON ADMIN E PROVA A MODIFICARE RUOLO ADMIN
            if not is_admin and utente_update.CHECK_ADMIN is not None:
                raise HTTPException(status_code=403, detail="Non hai i permessi per modificare il ruolo admin")

            # GEOCODIFICA
            coordinate_raw = utente_update.COORDINATE_UTENTE
            indirizzo = utente_update.INDIRIZZO_UTENTE
            try:

                # SE SOLO COORDINATE
                if coordinate_raw and not indirizzo:
                    indirizzo = indirizzo_da_coordinate(normalizza_coordinate_input(coordinate_raw))
                    risultato_verifica = verifica_coordinate_indirizzo(indirizzo, coordinate_raw)
                    distanza = risultato_verifica["distanza_metri"]
                    utente_update.INDIRIZZO_UTENTE = indirizzo

                # SE SOLO INDIRIZZO
                elif indirizzo and not coordinate_raw:
                    # Ottengo coordinate dall'indirizzo
                    risultato_verifica = verifica_coordinate_indirizzo(indirizzo, None)
                    utente_update.COORDINATE_UTENTE = risultato_verifica["coordinate"]
                    distanza = risultato_verifica["distanza_metri"]

                # SE ENTRAMBI
                elif indirizzo and coordinate_raw:
                    # Entrambi forniti: verifica distanza e coerenza
                    risultato_verifica = verifica_coordinate_indirizzo(indirizzo, coordinate_raw)
                    distanza = risultato_verifica["distanza_metri"]

                # SE NESSUN INDIRIZZO O COORDINATE
                else:
                    raise HTTPException(status_code=400, detail="È necessario fornire almeno COORDINATE_UTENTE o INDIRIZZO_UTENTE")

            # ERRORE DI GEOCODIFICA
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

            # SE COORDINATE MODIFICATE
            if utente_update.COORDINATE_UTENTE:

                # CONVERTI COORDINATE IN "POINT(lon lat)"
                try:
                    utente_update.COORDINATE_UTENTE = normalizza_coordinate_input(utente_update.COORDINATE_UTENTE)

                # ERRORE DI CONVERSIONE
                except ValueError as ve:
                    raise HTTPException(status_code=422, detail=str(ve))

            # QUERY DI AGGIORNAMENTO
            query = """
                UPDATE utente SET 
                EMAIL_UTENTE = COALESCE(%s, EMAIL_UTENTE),
                PASSWORD_UTENTE = COALESCE(%s, PASSWORD_UTENTE),
                NOME_UTENTE = COALESCE(%s, NOME_UTENTE),
                CHECK_ADMIN = COALESCE(%s, CHECK_ADMIN),
                INDIRIZZO_UTENTE = COALESCE(%s, INDIRIZZO_UTENTE),
                COORDINATE_UTENTE = COALESCE(ST_GeomFromText(%s, 4326), COORDINATE_UTENTE)
                WHERE ID_UTENTE = %s
            """

            # NORMALIZZAZIONE CAMPI
            utente_update.CHECK_ADMIN = normalizza_input_nullo(utente_update.CHECK_ADMIN, tipo="bool")
            utente_update.EMAIL_UTENTE = normalizza_input_nullo(utente_update.EMAIL_UTENTE, tipo="str")
            utente_update.PASSWORD_UTENTE = normalizza_input_nullo(utente_update.PASSWORD_UTENTE, tipo="str")
            utente_update.NOME_UTENTE = normalizza_input_nullo(utente_update.NOME_UTENTE, tipo="str")
            utente_update.INDIRIZZO_UTENTE = normalizza_input_nullo(utente_update.INDIRIZZO_UTENTE, tipo="str")

            # HASH NUOVA PASSWORD
            password_norm = utente_update.PASSWORD_UTENTE
            if password_norm:
                utente_update.PASSWORD_UTENTE = bcrypt.hashpw(
                    password_norm.encode('utf-8'), bcrypt.gensalt()
                ).decode('utf-8')
            else:
                utente_update.PASSWORD_UTENTE = None

            # VALORI DA AGGIORNARE
            valori = (
                utente_update.EMAIL_UTENTE,
                utente_update.PASSWORD_UTENTE,
                utente_update.NOME_UTENTE,
                utente_update.CHECK_ADMIN,
                utente_update.INDIRIZZO_UTENTE,
                utente_update.COORDINATE_UTENTE,
                ID_UTENTE
            )

            # ESECUZIONE QUERY
            cursor.execute(query, valori)
            connessione.commit()

            # VISUALIZZA UTENTE (NO PASSWORD)
            cursor.execute("""
                SELECT ID_UTENTE, EMAIL_UTENTE, NOME_UTENTE, CHECK_ADMIN, DATA_REGISTRAZIONE, INDIRIZZO_UTENTE,
                ST_AsText(COORDINATE_UTENTE) AS COORDINATE_UTENTE
                FROM utente
                WHERE ID_UTENTE = %s
            """, (ID_UTENTE,))
            result = cursor.fetchone()

            # CONVERSIONE TIMESTAMP E COORDINATE
            result_convertito = conversione([result])[0]

            # RISPOSTA JSON
            return JSONResponse({
                "message": f"Utente {ID_UTENTE} aggiornato con successo",
                "utente": result_convertito,
                "distanza_metri": round(distanza, 2) if distanza is not None else None
            })

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error updating event")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| ELIMINA UTENTE (7) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# DELETE /UTENTI/{ID_UTENTE}
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹
@app.delete("/UTENTI")
@app.delete("/UTENTI/{ID_UTENTE}")
async def delete_utente(request: Request, ID_UTENTE: int = None):

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:

            # VERIFICA SESSIONE
            id_sessione = request.session.get("ID_UTENTE")

            # DETERMINA ID_UTENTE DA ELIMINARE
            if ID_UTENTE is None:
                ID_UTENTE = id_sessione
            if ID_UTENTE is None:
                raise HTTPException(status_code=401, detail="Utente non autenticato")

            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # SE NON TROVATO
            cursor.execute("SELECT * FROM utente WHERE ID_UTENTE = %s", (ID_UTENTE,))
            utente = cursor.fetchone()
            if not utente:
                raise HTTPException(status_code=404, detail="Utente non trovato")
            
            # SE NON È ADMIN O NON È IL PROPRIO PROFILO
            if not is_admin and id_verificato != ID_UTENTE:
                raise HTTPException(status_code=403, detail="Non hai i permessi per eliminare questo utente")
            
            # ADMIN NON ELIMINA ADMIN
            if utente["CHECK_ADMIN"] == 1 and not is_admin:
                raise HTTPException(status_code=403, detail="Non puoi eliminare un altro admin")

            # ELIMINA EVENTI CREATI DALL'UTENTE (per evitare errori di foreign key)
            cursor.execute("DELETE FROM evento WHERE ID_UTENTE = %s", (ID_UTENTE,))

            # ELIMINA ISCRIZIONI DELL'UTENTE (se esistono altre FK)
            cursor.execute("DELETE FROM iscrizione WHERE ID_UTENTE = %s", (ID_UTENTE,))

            # ELIMINA UTENTE
            cursor.execute("DELETE FROM utente WHERE ID_UTENTE = %s", (ID_UTENTE,))
            connessione.commit()

            # LOGOUT SE STESSO UTENTE
            if ID_UTENTE == id_sessione:
                request.session.clear()

            # RISPOSTA JSON
            return JSONResponse({"message": f"Utente {ID_UTENTE} eliminato con successo da {id_verificato}"})

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error during user deletion")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| DETTAGLI ISCRIZIONE (8) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /ISCRIZIONI/{ID_EVENTO}/{ID_UTENTE}
@app.get("/ISCRIZIONI/{ID_EVENTO}/{ID_UTENTE}")
async def get_iscrizione_dettagliata(ID_EVENTO: int, ID_UTENTE: int):

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # QUERY DATI ISCRIZIONE
            query = """
                SELECT 
                    iscrizione.ID_EVENTO,
                    iscrizione.ID_UTENTE,
                    iscrizione.DATA_ISCRIZIONE,
                    evento.NOME_EVENTO,
                    evento.DATA_EVENTO,
                    utente.NOME_UTENTE
                FROM iscrizione
                JOIN evento ON iscrizione.ID_EVENTO = evento.ID_EVENTO
                JOIN utente ON iscrizione.ID_UTENTE = utente.ID_UTENTE
                WHERE iscrizione.ID_EVENTO = %s AND iscrizione.ID_UTENTE = %s
            """
            cursor.execute(query, (ID_EVENTO, ID_UTENTE))
            iscrizione = cursor.fetchone()

            # SE NON TROVATO
            if not iscrizione:
                raise HTTPException(status_code=404, detail="Iscrizione non trovata")

            # CONVERSIONE TIMESTAMP E COORDINATE
            iscrizione_convertita = conversione([iscrizione])[0]

            # RISPOSTA JSON
            return JSONResponse(content=iscrizione_convertita)

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error retrieving subscription details")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| FILTRO ISCRIZIONI (9) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /ISCRIZIONI?&ID_UTENTE=1&ID_EVENTO=1&DATA=01-01-2026_31-01-2026
# ℹ️ ID_EVENTO = {ID_EVENTO}
# ℹ️ ID_UTENTE = {ID_UTENTE}  
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)
@app.get("/ISCRIZIONI")
async def get_iscrizioni(request: Request):

    # PARAMETRI FILTRO
    params = request.query_params
    tipo = params.get("TIPO", "TUTTI").upper()  # default TUTTI
    id_utente_filtro = params.get("ID_UTENTE")
    id_evento_filtro = params.get("ID_EVENTO")
    data_filter = normalizza_input_nullo(params.get("DATA"), tipo="str")

    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # QUERY BASE ALL (ADMIN)
            if is_admin:
                query = """
                    SELECT iscrizione.ID_ISCRIZIONE, iscrizione.ID_UTENTE, iscrizione.ID_EVENTO, iscrizione.DATA_ISCRIZIONE,
                           utente.EMAIL_UTENTE, utente.NOME_UTENTE, utente.CHECK_ADMIN, utente.DATA_REGISTRAZIONE, utente.INDIRIZZO_UTENTE,
                           evento.DATA_EVENTO, evento.INDIRIZZO_EVENTO, ST_AsText(utente.COORDINATE_UTENTE) AS COORDINATE_UTENTE,
                           evento.NOME_EVENTO, evento.DESCRIZIONE_EVENTO, evento.DATA_EVENTO, evento.INDIRIZZO_EVENTO, evento.COSTO,
                           evento.CHECK_MAGGIORENNI, evento.PASSWORD_EVENTO, ST_AsText(evento.COORDINATE_EVENTO) AS COORDINATE_EVENTO
                    FROM iscrizione
                    JOIN utente ON iscrizione.ID_UTENTE = utente.ID_UTENTE
                    JOIN evento ON iscrizione.ID_EVENTO = evento.ID_EVENTO
                """
            # QUERY BASE PART (CREATORE EVENTO)
            elif id_verificato == id_sessione:
                query = """
                    SELECT iscrizione.ID_ISCRIZIONE, iscrizione.ID_UTENTE, iscrizione.ID_EVENTO, iscrizione.DATA_ISCRIZIONE,
                           utente.NOME_UTENTE, evento.NOME_EVENTO
                    FROM iscrizione
                    JOIN utente ON iscrizione.ID_UTENTE = utente.ID_UTENTE
                    JOIN evento ON iscrizione.ID_EVENTO = evento.ID_EVENTO
                """

            conditions = []
            values = []

            # SE NON ADMIN
            if not is_admin:

                # FILTRO TIPO (PROPRIO EVENTO)
                if tipo == "CREATI":
                    conditions.append("evento.ID_UTENTE = %s")
                    values.append(id_sessione)

            # FILTRO ID_UTENTE
            if id_utente_filtro:

                # SE ADMIN PUÒ VEDERE ISCRIZIONI DI ALTRI UTENTI
                if is_admin:
                    conditions.append("iscrizione.ID_UTENTE = %s")
                    values.append(id_utente_filtro)

                # SE NON ADMIN NON PUÒ VEDERE ISCRIZIONI DI ALTRI UTENTI
                else:
                    if str(id_utente_filtro) != str(id_sessione):
                        return JSONResponse(content={"errore": "Non hai i permessi per vedere le iscrizioni di altri utenti"}, status_code=403)
                    conditions.append("iscrizione.ID_UTENTE = %s")
                    values.append(id_utente_filtro)

            # FILTRO ID_EVENTO (PROPRIE ISCRIZIONI O ADMIN CON ALTRI UTENTI)  
            if id_evento_filtro:
                conditions.append("iscrizione.ID_EVENTO = %s")
                values.append(id_evento_filtro)

            # FILTRO DATA_ISCRIZIONE
            if data_filter:
                try:
                    condizioni_data, valori_data = genera_filtro_data(data_filter, "DATA_ISCRIZIONE")
                    conditions.extend(condizioni_data)
                    values.extend(valori_data)
                except HTTPException as e:
                    return JSONResponse(content={"errore": e.detail}, status_code=e.status_code)

            # AGGIUNTA CONDIZIONI
            if conditions:
                if "WHERE" in query:
                    query += " AND " + " AND ".join(conditions)
                else:
                    query += " WHERE " + " AND ".join(conditions)

            # ORDINO PER DATA_ISCRIZIONE DECRESCENTE
            query += " ORDER BY DATA_ISCRIZIONE DESC"

            # ESEGUO QUERY
            cursor.execute(query, tuple(values))
            iscrizioni = cursor.fetchall()

            # CONVERSIONE TIMESTAMP E COORDINATE
            iscrizioni_convertite = conversione(iscrizioni)

            return JSONResponse(content={"iscrizioni": iscrizioni_convertite})

    except mysql.connector.Error as err:
        logging.exception("Database error retrieving subscriptions")
        raise HTTPException(status_code=500, detail="Errore database durante il recupero iscrizioni")
    except Exception as e:
        logging.exception("Unexpected error retrieving subscriptions")
        raise HTTPException(status_code=500, detail="Errore interno inatteso")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CREA ISCRIZIONE (10) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# POST /ISCRIZIONI/{ID_EVENTO}/{ID_UTENTE}
# POST /ISCRIZIONI/{ID_EVENTO}  (ricava ID_UTENTE dalla sessione)
# 🡹 [⚠️GESTIONE PERMESSI E PASSWORD EVENTO⚠️] 🡹
@app.post("/ISCRIZIONI/{id_evento}")
@app.post("/ISCRIZIONI/{id_evento}/{id_utente}")
async def crea_iscrizione(id_evento: int, request: Request, id_utente: int = None):

    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")

    # SE NON AUTENTICATO
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")

    # SE ID_UTENTE NON FORNITO, USA LA SESSIONE
    if id_utente is None:
        id_utente = id_sessione

    # LEGGI DATI JSON (PASSWORD SE FORNITA)
    try:
        data = await request.json()
    except:
        data = {}

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # SE NON ADMIN O NON È IL PROPRIO PROFILO
            if not (is_admin or id_verificato == id_utente):
                raise HTTPException(status_code=403, detail="Permessi insufficienti")

            # VERIFICA ISCRIZIONE ESISTENTE
            query_check = "SELECT COUNT(*) as cnt FROM iscrizione WHERE ID_EVENTO=%s AND ID_UTENTE=%s"
            cursor.execute(query_check, (id_evento, id_utente))
            count = cursor.fetchone()['cnt']

            # SE ISCRIZIONE ESISTE
            if count > 0:
                raise HTTPException(status_code=409, detail="Iscrizione già esistente")

            # VERIFICA EVENTO E PASSWORD
            cursor.execute("SELECT ID_EVENTO, ID_UTENTE, PASSWORD_EVENTO, MAX_PARTECIPANTI, NOME_EVENTO, DATA_EVENTO, INDIRIZZO_EVENTO, COSTO, CHECK_MAGGIORENNI FROM evento WHERE ID_EVENTO = %s", (id_evento,))
            evento = cursor.fetchone()
            
            # SE EVENTO NON ESISTE
            if not evento:
                raise HTTPException(status_code=404, detail="Evento non trovato")
            
            # DATI EVENTO
            evento_creator = evento['ID_UTENTE']
            password_hash = evento['PASSWORD_EVENTO']
            max_partecipanti = evento['MAX_PARTECIPANTI']

            # VERIFICA PASSWORD SE EVENTO HA PASSWORD
            if password_hash and not is_admin and id_sessione != evento_creator:
                password_fornita = data.get("PASSWORD_EVENTO")
                
                # SE PASSWORD NON FORNITA
                if not password_fornita:
                    raise HTTPException(status_code=403, detail="Password richiesta per iscriversi a questo evento")
                
                # VERIFICA PASSWORD
                if not bcrypt.checkpw(password_fornita.encode('utf-8'), password_hash.encode('utf-8')):
                    raise HTTPException(status_code=403, detail="Password non corretta")

            # VERIFICA LIMITE PARTECIPANTI
            if max_partecipanti and max_partecipanti > 0:
                cursor.execute("SELECT COUNT(*) as cnt FROM iscrizione WHERE ID_EVENTO = %s", (id_evento,))
                iscritti = cursor.fetchone()['cnt']
                if iscritti >= max_partecipanti:
                    raise HTTPException(status_code=409, detail="Limite massimo di partecipanti raggiunto")

            # CREAZIONE ISCRIZIONE
            query_insert = "INSERT INTO iscrizione (ID_EVENTO, ID_UTENTE, DATA_ISCRIZIONE) VALUES (%s, %s, NOW())"
            cursor.execute(query_insert, (id_evento, id_utente))
            connessione.commit()

            # CONVERSIONE DATETIME PER JSON
            evento_convertito = conversione([evento])[0]

            # RISPOSTA JSON
            return JSONResponse({
                "successo": True, 
                "messaggio": "Iscrizione creata",
                "evento": {
                    "ID_EVENTO": evento_convertito['ID_EVENTO'],
                    "NOME_EVENTO": evento_convertito.get('NOME_EVENTO'),
                    "DATA_EVENTO": evento_convertito.get('DATA_EVENTO'),
                    "INDIRIZZO_EVENTO": evento_convertito.get('INDIRIZZO_EVENTO'),
                    "COSTO": evento_convertito.get('COSTO'),
                    "CHECK_MAGGIORENNI": evento_convertito.get('CHECK_MAGGIORENNI'),
                    "MAX_PARTECIPANTI": evento_convertito.get('MAX_PARTECIPANTI')
                },
                "ID_UTENTE": id_utente
            })

    # ERRORE NELLA QUERY
    except HTTPException:
        # RISPONDI CON L'ERRORE GIÀ DEFINITO
        raise

    # ERRORE GENERICO
    except (mysql.connector.Error, Exception) as err:
        connessione.rollback()
        logging.exception("Database error creating subscription")
        raise HTTPException(status_code=500, detail="Errore durante la creazione iscrizione")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CANCELLA ISCRIZIONE (11) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# DELETE /ISCRIZIONI/{ID_EVENTO}/{ID_UTENTE}
# DELETE /ISCRIZIONI/{ID_EVENTO}  (ricava ID_UTENTE dalla sessione)
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹
@app.delete("/ISCRIZIONI/{id_evento}")
@app.delete("/ISCRIZIONI/{id_evento}/{id_utente}")
async def elimina_iscrizione(id_evento: int, request: Request, id_utente: int = None):

    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")

    # SE NON AUTENTICATO
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")

    # SE ID_UTENTE NON FORNITO, USA LA SESSIONE
    if id_utente is None:
        id_utente = id_sessione

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # SE NON ADMIN O NON È IL PROPRIO PROFILO
            if not (is_admin or id_verificato == id_utente):
                raise HTTPException(status_code=403, detail="Permessi insufficienti")

            # VERIFICA ISCRIZIONE ESISTENTE
            query_check = "SELECT COUNT(*) as cnt FROM iscrizione WHERE ID_EVENTO=%s AND ID_UTENTE=%s"
            cursor.execute(query_check, (id_evento, id_utente))
            count = cursor.fetchone()['cnt']

            # SE ISCRIZIONE NON ESISTE
            if count == 0:
                raise HTTPException(status_code=404, detail="Iscrizione non trovata")

            # ELIMINA ISCRIZIONE
            query_delete = "DELETE FROM iscrizione WHERE ID_EVENTO=%s AND ID_UTENTE=%s"
            cursor.execute(query_delete, (id_evento, id_utente))
            connessione.commit()

            # RISPOSTA JSON
            return JSONResponse({"successo": True, "messaggio": "Iscrizione eliminata"})

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        connessione.rollback()
        logging.exception("Database error deleting subscription")
        raise HTTPException(status_code=500, detail="Errore database durante l'eliminazione iscrizione")
    except Exception as e:
        connessione.rollback()
        logging.exception("Unexpected error deleting subscription")
        raise HTTPException(status_code=500, detail="Errore interno inatteso")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CANCELLA ISCRIZIONI FILTRATE (12) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# DELETE /ISCRIZIONI?ID_UTENTE=1&ID_EVENTO=1&DATA=01-01-2026_31-01-2026
# ℹ️ ID_EVENTO = {ID_EVENTO}
# ℹ️ ID_UTENTE = {ID_UTENTE}
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)
# 🡹 [⚠️GESTIONE PERMESSI ADMIN E CREATORE⚠️] 🡹
@app.delete("/ISCRIZIONI")
async def elimina_iscrizioni(request: Request):

    # PARAMETRI FILTRO
    params = request.query_params
    id_utente_filtro = params.get("ID_UTENTE")
    id_evento_filtro = params.get("ID_EVENTO")
    data_filter = normalizza_input_nullo(params.get("DATA"), tipo="str")

    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # SE NON ADMIN E RICHIESTO ID_EVENTO
            is_creatore = False
            if not is_admin and id_evento_filtro:
                cursor.execute("SELECT ID_UTENTE FROM evento WHERE ID_EVENTO = %s", (id_evento_filtro,))
                row = cursor.fetchone()

                # SE PROPRIETARIO DELL'EVENTO
                if row and row["ID_UTENTE"] == id_sessione:
                    is_creatore = True

            # SE NON ADMIN O NON È IL PROPRIO PROFILO
            if not (is_admin or is_creatore):
                raise HTTPException(status_code=403, detail="Permessi insufficienti")

            # COSTRUZIONE QUERY
            query = "DELETE FROM iscrizione"
            conditions = []
            values = []

            # SE SOLO ID_EVENTO FORNITO, RICAVA ID_UTENTE DALLA SESSIONE
            if id_evento_filtro and not id_utente_filtro:
                id_utente_filtro = id_sessione

            # FILTRO ID_UTENTE
            if id_utente_filtro:
                conditions.append("ID_UTENTE = %s")
                values.append(id_utente_filtro)

            # FILTRO ID_EVENTO
            if id_evento_filtro:
                conditions.append("ID_EVENTO = %s")
                values.append(id_evento_filtro)

            # FILTRO DATA_ISCRIZIONE
            if data_filter:
                try:
                    condizioni_data, valori_data = genera_filtro_data(data_filter, "DATA_ISCRIZIONE")
                    conditions.extend(condizioni_data)
                    values.extend(valori_data)

                # ERRORE DATA
                except HTTPException as e:
                    raise e

            # SE NON CI SONO FILTRI
            if not conditions:
                raise HTTPException(status_code=400, detail="Serve almeno un filtro per l'eliminazione")

            # AGGIUNTA CONDIZIONI
            query += " WHERE " + " AND ".join(conditions)

            # ESECUZIONE ELIMINAZIONE
            cursor.execute(query, tuple(values))
            connessione.commit()
            deleted_count = cursor.rowcount

            # RISPOSTA JSON
            return JSONResponse({"successo": True, "messaggi": f"{deleted_count} iscrizioni eliminate"})
    
    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        connessione.rollback()
        logging.exception("Database error deleting multiple subscriptions")
        raise HTTPException(status_code=500, detail="Errore database durante l'eliminazione iscrizioni")
    except Exception as e:
        connessione.rollback()
        logging.exception("Unexpected error deleting multiple subscriptions")
        raise HTTPException(status_code=500, detail="Errore interno inatteso")
        
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| EVENTO SELEZIONATO (13) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /EVENTI/{ID_EVENTO}
@app.get("/EVENTI/{ID_EVENTO}")
async def get_evento_selezionato(ID_EVENTO: int):

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            # QUERY DATI EVENTO
            query = """
                SELECT 
                    evento.ID_EVENTO,
                    evento.NOME_EVENTO,
                    evento.DESCRIZIONE_EVENTO,
                    evento.DATA_EVENTO,
                    evento.INDIRIZZO_EVENTO,
                    evento.COSTO,
                    evento.CHECK_MAGGIORENNI,
                    evento.PASSWORD_EVENTO,
                    evento.MAX_PARTECIPANTI,
                    evento.COORDINATE_EVENTO,
                    utente.NOME_UTENTE,
                    categoria.NOME_CATEGORIA AS CATEGORIA
                FROM evento
                JOIN utente ON evento.ID_UTENTE = utente.ID_UTENTE
                LEFT JOIN evento_categoria ON evento.ID_EVENTO = evento_categoria.ID_EVENTO
                LEFT JOIN categoria ON evento_categoria.ID_CATEGORIA = categoria.ID_CATEGORIA
                WHERE evento.ID_EVENTO = %s
            """
            cursor.execute(query, (ID_EVENTO,))
            risultati = cursor.fetchall()

            # SE NON TROVATO
            if not risultati:
                raise HTTPException(status_code=404, detail=f"Nessun evento con ID {ID_EVENTO} trovato")

            # AGGREGAZIONE CATEGORIE DA RIGHE DUPLICATE
            evento_dict = None
            categorie = set()
            
            for row in risultati:
                if evento_dict is None:
                    evento_dict = {
                        'ID_EVENTO': row['ID_EVENTO'],
                        'NOME_EVENTO': row['NOME_EVENTO'],
                        'DESCRIZIONE_EVENTO': row['DESCRIZIONE_EVENTO'],
                        'DATA_EVENTO': row['DATA_EVENTO'],
                        'INDIRIZZO_EVENTO': row['INDIRIZZO_EVENTO'],
                        'COSTO': row['COSTO'],
                        'CHECK_MAGGIORENNI': row['CHECK_MAGGIORENNI'],
                        'PASSWORD_EVENTO': row['PASSWORD_EVENTO'],
                        'MAX_PARTECIPANTI': row['MAX_PARTECIPANTI'],
                        'COORDINATE_EVENTO': row['COORDINATE_EVENTO'],
                        'NOME_UTENTE': row['NOME_UTENTE']
                    }
                
                if row['CATEGORIA']:
                    categorie.add(row['CATEGORIA'])
            
            evento_dict['CATEGORIE'] = list(categorie) if categorie else []

            # CONVERSIONE TIMESTAMP E COORDINATE
            evento_convertito = conversione([evento_dict])[0]

            # RISPOSTA JSON
            return JSONResponse(content=evento_convertito)

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error retrieving event details")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CREA EVENTO (14) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# POST /EVENTI/{ID_UTENTE}
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹
@app.post("/EVENTI")
@app.post("/EVENTI/{ID_UTENTE}")
async def crea_evento(request: Request, ID_UTENTE: Optional[int] = None):
    # SESSIONE UTENTE
    id_sessione = request.session.get("ID_UTENTE")
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")

    # DATI JSON
    data = await request.json()
    required_keys = ["NOME_EVENTO", "DESCRIZIONE_EVENTO", "DATA_EVENTO"]
    for key in required_keys:
        if key not in data:
            raise HTTPException(status_code=422, detail=f"Chiave mancante: {key}")

    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # SE NON INSERITO ID_UTENTE
            if ID_UTENTE is None:
                ID_UTENTE = id_verificato
            elif not is_admin and id_verificato != ID_UTENTE:
                raise HTTPException(status_code=403, detail="Non hai i permessi per modificare questo utente")

            # GESTIONE POSIZIONE EVENTO
            coordinate = normalizza_input_nullo(data.get("COORDINATE_EVENTO"), tipo="str")
            indirizzo = normalizza_input_nullo(data.get("INDIRIZZO_EVENTO"), tipo="str")
            distanza = None
            coordinate_db = None

            # SOLO COORDINATE
            if coordinate and not indirizzo:
                try:
                    coordinate_db = normalizza_coordinate_input(coordinate)
                    indirizzo = indirizzo_da_coordinate(coordinate_db)
                except Exception:
                    raise HTTPException(status_code=422, detail="Formato COORDINATE_EVENTO non valido. Usa 'lat lon' come stringa.")

            # SOLO INDIRIZZO
            elif indirizzo and not coordinate:
                risultato_geo = verifica_coordinate_indirizzo(indirizzo)
                coordinate = risultato_geo["coordinate"]
                distanza = risultato_geo["distanza_metri"]
                coordinate_db = normalizza_coordinate_input(coordinate)

            # ENTRAMBI
            elif indirizzo and coordinate:
                try:
                    coordinate_db = normalizza_coordinate_input(coordinate)
                except Exception:
                    raise HTTPException(status_code=422, detail="Formato COORDINATE_EVENTO non valido. Usa 'lat lon' come stringa.")
                risultato_geo = verifica_coordinate_indirizzo(indirizzo, coordinate)
                coordinate = risultato_geo["coordinate"]
                distanza = risultato_geo["distanza_metri"]
                coordinate_db = normalizza_coordinate_input(coordinate)

            # MANCANO ENTRAMBI
            else:
                raise HTTPException(status_code=400, detail="È necessario fornire almeno INDIRIZZO_EVENTO o COORDINATE_EVENTO")

            # HASH PASSWORD EVENTO (se fornita)
            password_evento = normalizza_input_nullo(data.get("PASSWORD_EVENTO"), tipo="str")
            hashed_password = None
            if password_evento:
                hashed_password = bcrypt.hashpw(password_evento.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # QUERY INSERIMENTO
            query = """
                INSERT INTO evento (
                    NOME_EVENTO, DESCRIZIONE_EVENTO, DATA_EVENTO, INDIRIZZO_EVENTO, COSTO,
                    CHECK_MAGGIORENNI, PASSWORD_EVENTO, COORDINATE_EVENTO, MAX_PARTECIPANTI, ID_UTENTE
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s, %s)
            """

            # NORMALIZZAZIONE CAMPI
            costo = normalizza_input_nullo(data.get("COSTO", 0.0), tipo="num")
            if costo is None:
                costo = 0.0
            check_maggiorenni = normalizza_input_nullo(data.get("CHECK_MAGGIORENNI", False), tipo="bool")
            if check_maggiorenni is None:
                check_maggiorenni = False
            max_partecipanti = normalizza_input_nullo(data.get("MAX_PARTECIPANTI", 0), tipo="num")
            if max_partecipanti is None:
                max_partecipanti = 0
            password_evento = normalizza_input_nullo(data.get("PASSWORD_EVENTO"), tipo="str")
            hashed_password = None
            if password_evento:
                hashed_password = bcrypt.hashpw(password_evento.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # VALORI INSERIMENTO
            valori = (
                data["NOME_EVENTO"],
                data["DESCRIZIONE_EVENTO"],
                data["DATA_EVENTO"],
                indirizzo,
                costo,
                check_maggiorenni,
                hashed_password,
                coordinate_db,
                max_partecipanti,
                ID_UTENTE
            )
            cursor.execute(query, valori)
            connessione.commit()
            ID_EVENTO = cursor.lastrowid

            # ASSOCIAZIONE CATEGORIA/E
            categorie = []
            
            # INPUT CATEGORIE
            categorie_input = data.get("CATEGORIE") or data.get("NOME_CATEGORIA")
            
            if categorie_input:

                # GESTIONE SINGOLO VALORE O LISTA
                if isinstance(categorie_input, str):
                    categorie_input = [categorie_input]

                # LIMITAZIONE MASSIMA 3 CATEGORIE
                if len(categorie_input) > 3:
                    raise HTTPException(status_code=422, detail="Al massimo 3 categorie sono permesse")

                # ASSOCIAZIONE CATEGORIE
                for nome_cat in categorie_input:
                    nome_cat = normalizza_input_nullo(nome_cat, tipo="str")
                    if nome_cat:
                        query_cat = "SELECT ID_CATEGORIA FROM categoria WHERE NOME_CATEGORIA = %s"
                        cursor.execute(query_cat, (nome_cat,))
                        row = cursor.fetchone()
                        if not row:
                            raise HTTPException(status_code=404, detail=f"Categoria '{nome_cat}' non esistente")
                        id_categoria = row["ID_CATEGORIA"]
                        query_assoc = "INSERT INTO evento_categoria (ID_EVENTO, ID_CATEGORIA) VALUES (%s, %s)"
                        cursor.execute(query_assoc, (ID_EVENTO, id_categoria))
                        categorie.append(nome_cat)

                connessione.commit()

            # RISPOSTA JSON
            evento_response = {
                "ID_EVENTO": ID_EVENTO,
                "NOME_EVENTO": data["NOME_EVENTO"],
                "DESCRIZIONE_EVENTO": data["DESCRIZIONE_EVENTO"],
                "DATA_EVENTO": data["DATA_EVENTO"],
                "INDIRIZZO_EVENTO": indirizzo,
                "COSTO": costo,
                "CHECK_MAGGIORENNI": check_maggiorenni,
                "MAX_PARTECIPANTI": max_partecipanti,
                "COORDINATE_EVENTO": coordinate,
                "CATEGORIE": categorie,
                "distanza_coordinate_indirizzo": distanza
            }
            return JSONResponse({
                "message": "Evento creato con successo",
                "evento": evento_response,
                "creato_da": id_verificato
            })

    # ERRORE NELLA QUERY O GESTIONE DATI
    except mysql.connector.Error as err:
        logging.exception("Database error creating event")
        raise HTTPException(status_code=500, detail="Errore interno")
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| MODIFICA EVENTO (15) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# PUT /EVENTI/{ID_EVENTO}
@app.put("/EVENTI/{ID_EVENTO}")
async def aggiorna_evento(ID_EVENTO: int, request: Request):
    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")
    
    # INPUT JSON
    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"JSON non valido: {str(e)}")

    try:
        with connessione.cursor(dictionary=True) as cursor:
            distanza = None
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # VERIFICA ID_EVENTO
            cursor.execute("SELECT ID_UTENTE FROM evento WHERE ID_EVENTO = %s", (ID_EVENTO,))
            evento = cursor.fetchone()
            if not evento:
                raise HTTPException(status_code=404, detail="Evento non trovato")

            # SE NON ADMIN O NON È IL PROPRIO PROFILO
            id_creator = evento["ID_UTENTE"]
            if not is_admin and id_creator != id_verificato:
                raise HTTPException(status_code=403, detail="Non hai i permessi per modificare questo evento")

            # DATI EVENTO
            nome = normalizza_input_nullo(data.get("NOME_EVENTO"), tipo="str")
            descrizione = normalizza_input_nullo(data.get("DESCRIZIONE_EVENTO"), tipo="str")
            data_evento = normalizza_input_nullo(data.get("DATA_EVENTO"), tipo="str")
            indirizzo = normalizza_input_nullo(data.get("INDIRIZZO_EVENTO"), tipo="str")
            costo = data.get("COSTO")
            max_partecipanti = data.get("MAX_PARTECIPANTI")
            check_maggiorenni = data.get("CHECK_MAGGIORENNI")
            coordinate = normalizza_input_nullo(data.get("COORDINATE_EVENTO"), tipo="str")
            nome_categoria = normalizza_input_nullo(data.get("NOME_CATEGORIA"), tipo="str")
            id_categoria = None

            # VERIFICA CATEGORIA
            if nome_categoria is not None:
                cursor.execute("SELECT ID_CATEGORIA FROM categoria WHERE NOME_CATEGORIA = %s", (nome_categoria,))
                row = cursor.fetchone()
                if not row:
                    raise HTTPException(status_code=404, detail=f"Categoria '{nome_categoria}' non trovata")
                id_categoria = row["ID_CATEGORIA"]

            # GEOCODING
            try:
                if indirizzo or coordinate:
                    if coordinate and not indirizzo:
                        indirizzo = indirizzo_da_coordinate(normalizza_coordinate_input(coordinate))
                        verifica = verifica_coordinate_indirizzo(indirizzo, coordinate)
                        distanza = verifica["distanza_metri"]
                        data["INDIRIZZO_EVENTO"] = indirizzo
                    elif indirizzo and not coordinate:
                        verifica = verifica_coordinate_indirizzo(indirizzo, None)
                        coordinate = verifica["coordinate"]
                        distanza = verifica["distanza_metri"]
                        data["COORDINATE_EVENTO"] = coordinate
                    elif indirizzo and coordinate:
                        verifica = verifica_coordinate_indirizzo(indirizzo, coordinate)
                        distanza = verifica["distanza_metri"]
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

            # SE FORNITE COORDINATE
            coordinate_geom = None
            if coordinate:
                try:
                    coordinate_geom = normalizza_coordinate_input(data["COORDINATE_EVENTO"])
                except ValueError as ve:
                    raise HTTPException(status_code=422, detail=str(ve))

            # HASH PASSWORD EVENTO
            password_evento_norm = normalizza_input_nullo(data.get("PASSWORD_EVENTO"), tipo="str")
            hashed_password = None
            if password_evento_norm:
                hashed_password = bcrypt.hashpw(password_evento_norm.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # QUERY AGGIORNAMENTO
            query = """
                UPDATE evento SET 
                    NOME_EVENTO = COALESCE(%s, NOME_EVENTO),
                    DESCRIZIONE_EVENTO = COALESCE(%s, DESCRIZIONE_EVENTO),
                    DATA_EVENTO = COALESCE(%s, DATA_EVENTO),
                    INDIRIZZO_EVENTO = COALESCE(%s, INDIRIZZO_EVENTO),
                    COSTO = COALESCE(%s, COSTO),
                    MAX_PARTECIPANTI = COALESCE(%s, MAX_PARTECIPANTI),
                    CHECK_MAGGIORENNI = COALESCE(%s, CHECK_MAGGIORENNI),
                    COORDINATE_EVENTO = COALESCE(ST_GeomFromText(%s, 4326), COORDINATE_EVENTO),
                    PASSWORD_EVENTO = COALESCE(%s, PASSWORD_EVENTO)
                WHERE ID_EVENTO = %s
            """

            # ESECUZIONE QUERY
            cursor.execute(query, (
                nome,
                descrizione,
                data_evento,
                indirizzo,
                costo,
                max_partecipanti,
                check_maggiorenni,
                coordinate_geom,
                hashed_password,
                ID_EVENTO
            ))
            connessione.commit()

            # AGGIORNA/IMPOSTA CATEGORIE EVENTO (supporta CATEGORIE list o NOME_CATEGORIA singolo)
            categorie_input = data.get("CATEGORIE") if "CATEGORIE" in data else data.get("NOME_CATEGORIA")
            if categorie_input is not None:
                # normalize to list
                if isinstance(categorie_input, str):
                    categorie_input = [categorie_input]

                # LIMITAZIONE MASSIMA 3 CATEGORIE
                if len(categorie_input) > 3:
                    raise HTTPException(status_code=422, detail="Al massimo 3 categorie sono permesse")

                # RISOLVI ID CATEGORIE E PREPARA INSERIMENTO
                ids_categorie = []
                nomi_categorie = []
                for nome_cat in categorie_input:
                    nome_cat = normalizza_input_nullo(nome_cat, tipo="str")
                    if not nome_cat:
                        continue
                    cursor.execute("SELECT ID_CATEGORIA FROM categoria WHERE NOME_CATEGORIA = %s", (nome_cat,))
                    row = cursor.fetchone()
                    if not row:
                        raise HTTPException(status_code=404, detail=f"Categoria '{nome_cat}' non trovata")
                    ids_categorie.append(row["ID_CATEGORIA"])
                    nomi_categorie.append(nome_cat)

                # RIMUOVI ASSOCIAZIONI CORRENTI E SOSTITUISCI CON LE NUOVE
                cursor.execute("DELETE FROM evento_categoria WHERE ID_EVENTO = %s", (ID_EVENTO,))
                for id_cat in ids_categorie:
                    cursor.execute(
                        "INSERT INTO evento_categoria (ID_EVENTO, ID_CATEGORIA) VALUES (%s, %s)",
                        (ID_EVENTO, id_cat)
                    )
                connessione.commit()

            # VERIFICA AGGIORNAMENTO
            cursor.execute("""
                SELECT evento.ID_EVENTO, evento.NOME_EVENTO, evento.DESCRIZIONE_EVENTO, evento.DATA_EVENTO, evento.INDIRIZZO_EVENTO, evento.COSTO, evento.MAX_PARTECIPANTI,
                       evento.CHECK_MAGGIORENNI, ST_AsText(evento.COORDINATE_EVENTO) AS COORDINATE_EVENTO,
                       categoria.NOME_CATEGORIA AS CATEGORIA
                FROM evento
                LEFT JOIN evento_categoria ON evento.ID_EVENTO = evento_categoria.ID_EVENTO
                LEFT JOIN categoria ON evento_categoria.ID_CATEGORIA = categoria.ID_CATEGORIA
                WHERE evento.ID_EVENTO = %s
            """, (ID_EVENTO,))
            risultati = cursor.fetchall()

            # SE NON TROVATO
            if not risultati:
                raise HTTPException(status_code=404, detail="Evento non trovato dopo aggiornamento")

            # AGGREGAZIONE CATEGORIE DA RIGHE DUPLICATE
            evento_aggiornato = None
            categorie = set()
            
            for row in risultati:
                if evento_aggiornato is None:
                    evento_aggiornato = {
                        'ID_EVENTO': row['ID_EVENTO'],
                        'NOME_EVENTO': row['NOME_EVENTO'],
                        'DESCRIZIONE_EVENTO': row['DESCRIZIONE_EVENTO'],
                        'DATA_EVENTO': row['DATA_EVENTO'],
                        'INDIRIZZO_EVENTO': row['INDIRIZZO_EVENTO'],
                        'COSTO': row['COSTO'],
                        'CHECK_MAGGIORENNI': row['CHECK_MAGGIORENNI'],
                        'MAX_PARTECIPANTI': row['MAX_PARTECIPANTI'],
                        'COORDINATE_EVENTO': row['COORDINATE_EVENTO']
                    }
                
                if row['CATEGORIA']:
                    categorie.add(row['CATEGORIA'])
            
            evento_aggiornato['CATEGORIE'] = list(categorie) if categorie else []

            # CONVERSIONE TIMESTAMP E COORDINATE
            evento_convertito = conversione([evento_aggiornato])[0]

            # RISPOSTA JSON
            return JSONResponse({
                "message": f"Evento {ID_EVENTO} aggiornato con successo",
                "evento": evento_convertito,
                "modificato_da": id_verificato,
                "distanza_metri": round(distanza, 2) if distanza is not None else None
            })
    
    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error updating event")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CANCELLA EVENTO (16) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# DELETE /EVENTI/{ID_EVENTO}
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹
@app.delete("/EVENTI/{ID_EVENTO}")
async def elimina_evento(ID_EVENTO: int, request: Request):
    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")

    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # VERIFICA ID_EVENTO
            cursor.execute("SELECT ID_UTENTE FROM evento WHERE ID_EVENTO = %s", (ID_EVENTO,))
            evento = cursor.fetchone()
            if not evento:
                raise HTTPException(status_code=404, detail="Evento non trovato")
            id_creatore = evento["ID_UTENTE"]

            # SE NON ADMIN O NON È IL PROPRIO PROFILO
            if not is_admin and id_creatore != id_verificato:
                raise HTTPException(status_code=403, detail="Non hai i permessi per eliminare questo evento")

            # ELIMINA EVENTO
            cursor.execute("DELETE FROM evento WHERE ID_EVENTO = %s", (ID_EVENTO,))
            connessione.commit()

            # RISPOSTA JSON
            return JSONResponse({
                "message": f"Evento {ID_EVENTO} eliminato con successo",
                "eliminato_da": id_verificato
            })
    
    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error deleting event")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CANCELLA EVENTI FILTRATI (17) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# DELETE /EVENTI?TIPO=TUTTI&ID_UTENTE=1&DATA=01-01-2026_31-01-2026
# ℹ️ ID_UTENTE = {ID_UTENTE}
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹     
@app.delete("/EVENTI")
async def elimina_eventi(
    request: Request,
    ID_UTENTE: Optional[int] = None,
    DATA: Optional[str] = None
):
    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")
    
    # NORMALIZZA DATA
    DATA = normalizza_input_nullo(DATA, tipo="str")

    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # SE NON ADMIN E RICHIESTO ID_UTENTE
            if not is_admin and ID_UTENTE and ID_UTENTE != id_verificato:
                raise HTTPException(status_code=403, detail="Non hai i permessi per eliminare eventi di altri utenti")

            # SE NON INSERITO ID_UTENTE
            if ID_UTENTE is None:
                ID_UTENTE = id_verificato

            # COSTRUZIONE QUERY
            condizioni = []
            valori = []

            # FILTRO ID_UTENTE
            if ID_UTENTE:
                condizioni.append("ID_UTENTE = %s")
                valori.append(ID_UTENTE)

            # FILTRO DATA_EVENTO
            if DATA:
                condizioni_data, valori_data = genera_filtro_data(DATA, "DATA_EVENTO")
                condizioni.extend(condizioni_data)
                valori.extend(valori_data)

            # AGGIUNTA CONDIZIONI
            where_clause = f"WHERE {' AND '.join(condizioni)}" if condizioni else ""
            query_verifica = f"SELECT COUNT(*) AS n FROM evento {where_clause}"
            cursor.execute(query_verifica, tuple(valori))
            count = cursor.fetchone()["n"]

            # SE NON TROVATI EVENTI
            if count == 0:
                raise HTTPException(status_code=404, detail="Nessun evento corrispondente ai criteri")

            # ELIMINA EVENTI
            query_delete = f"DELETE FROM evento {where_clause}"
            cursor.execute(query_delete, tuple(valori))
            connessione.commit()

            # RISPOSTA JSON
            return JSONResponse({
                "message": f"{count} eventi eliminati con successo",
                "eliminato_da": id_verificato,
                "criteri": {
                    "ID_UTENTE": ID_UTENTE,
                    "DATA": DATA
                }
            })

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error deleting multiple events")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| EVENTI FILTRATI (17) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /EVENTI?&ID_UTENTE=1&ISCRITTO=True&MAGGIORENNI=True&DATA=01-01-2026_31-01-2026&PER_ALFABETO=>&PREZZO=10_50&CATEGORIA=CONCERTO&DISTANZA=1_50&RICERCA=PIZZA
# ℹ️ ID_UTENTE = {ID_UTENTE}
# ℹ️ ISCRITTO = [True, False]
# ℹ️ MAGGIORENNI = [True, False]
# ℹ️ DATA = [>{DD-MM-YYYY}, <{DD-MM-YYYY}, >={DD-MM-YYYY}, <={DD-MM-YYYY}, {DD-MM-YYYY}]      (DATA DI ISCRIZIONE)
# ℹ️ ALFABETO = [<, >]
# ℹ️ PREZZO = [<{PREZZO}, >{PREZZO}, {PREZZO}]
# ℹ️ CATEGORIA = [CONCERTO, ARTE, SPORT, CIBO, CINEMA, CERIMONIA, INTRATTENIMENTO, FORMAZIONE, MOSTRA]
# ℹ️ DISTANZA = [<{INSERIMENTO(Km)}, >{INSERIMENTO(Km)}, {INSERIMENTO(Km)}]
# ℹ️ RICERCA = {...NOME...}
@app.get("/EVENTI")
async def get_eventi(
    request: Request,
    ID_UTENTE: Optional[int] = None,
    ISCRITTO: Optional[bool] = None,
    MAGGIORENNI: Optional[bool] = None,
    HAS_PASSWORD: Optional[bool] = None,
    DATA: Optional[str] = None,
    ALFABETO: Optional[str] = None,
    PREZZO: Optional[str] = None,
    CATEGORIA: Optional[str] = None,
    DISTANZA: Optional[str] = None,
    RICERCA: Optional[str] = None
):
    # VERIFICA SESSIONE
    id_sessione = request.session.get("ID_UTENTE")

    # NORMALIZZA PARAMETRI INPUT
    DATA = normalizza_input_nullo(DATA, tipo="str")
    ALFABETO = normalizza_input_nullo(ALFABETO, tipo="str")
    PREZZO = normalizza_input_nullo(PREZZO, tipo="str")
    CATEGORIA = normalizza_input_nullo(CATEGORIA, tipo="str")
    DISTANZA = normalizza_input_nullo(DISTANZA, tipo="str")
    RICERCA = normalizza_input_nullo(RICERCA, tipo="str")
    ISCRITTO = normalizza_input_nullo(ISCRITTO, tipo="bool")
    MAGGIORENNI = normalizza_input_nullo(MAGGIORENNI, tipo="bool")
    HAS_PASSWORD = normalizza_input_nullo(HAS_PASSWORD, tipo="bool")

    try:
        with connessione.cursor(dictionary=True) as cursor:
            # VERIFICA ADMIN
            id_verificato, _ = verifica_admin(id_sessione, cursor)

            # Se anonimo, non filtrare per utente
            if ID_UTENTE is None and id_verificato is not None:
                ID_UTENTE = id_verificato

            condizioni = []
            valori = []

            # JOIN PER CATEGORIA
            join_categoria = """
                LEFT JOIN evento_categoria ON evento.ID_EVENTO = evento_categoria.ID_EVENTO
                LEFT JOIN categoria ON evento_categoria.ID_CATEGORIA = categoria.ID_CATEGORIA
            """

            # FILTRO ISCRITTO
            if ISCRITTO is not None:
                if ISCRITTO:
                    condizioni.append("evento.ID_EVENTO IN (SELECT ID_EVENTO FROM partecipazione WHERE ID_UTENTE = %s)")
                    valori.append(ID_UTENTE)
                else:
                    condizioni.append("evento.ID_EVENTO NOT IN (SELECT ID_EVENTO FROM partecipazione WHERE ID_UTENTE = %s)")
                    valori.append(ID_UTENTE)

            # FILTRO MAGGIORENNI
            if MAGGIORENNI is not None:
                condizioni.append("evento.CHECK_MAGGIORENNI = %s")
                valori.append(MAGGIORENNI)

            # FILTRO PASSWORD
            if HAS_PASSWORD is not None:
                if HAS_PASSWORD:
                    condizioni.append("evento.PASSWORD_EVENTO IS NOT NULL AND evento.PASSWORD_EVENTO != ''")
                else:
                    condizioni.append("(evento.PASSWORD_EVENTO IS NULL OR evento.PASSWORD_EVENTO = '')")

            # FILTRO DATA
            if DATA:
                condizioni_data, valori_data = genera_filtro_data(DATA, "evento.DATA_EVENTO")
                condizioni.extend(condizioni_data)
                valori.extend(valori_data)
            
            # DA OGGI IN POI
            condizioni.append("evento.DATA_EVENTO >= %s")
            valori.append(date.today())

            # FILTRO ORDINE ALFABETO
            order_clause = "ORDER BY evento.DATA_EVENTO ASC"  # default
            if ALFABETO:
                # Valida operatore con whitelist
                allowed = ALLOWED_SQL_OPERATORS.get("ALFABETO", [])
                if ALFABETO.strip() not in allowed:
                    raise HTTPException(status_code=400, detail=f"Operatore ALFABETO non valido: '{ALFABETO}'. Usa: {', '.join(allowed)}")
                if ALFABETO == ">":
                    order_clause = "ORDER BY evento.NOME_EVENTO ASC, evento.DATA_EVENTO ASC"   # A→Z, poi per data
                else:
                    order_clause = "ORDER BY evento.NOME_EVENTO DESC, evento.DATA_EVENTO ASC"  # Z→A, poi per data

            # FILTRO PREZZO
            if PREZZO:

                # RANGE MIN_MAX
                if "_" in PREZZO:
                    parts = PREZZO.split("_")
                    if len(parts) != 2:
                        raise HTTPException(status_code=400, detail="Intervallo PREZZO non valido: usare 'min_max' (es. 10_20)")
                    try:
                        p1 = float(parts[0].strip())
                        p2 = float(parts[1].strip())
                    except ValueError:
                        raise HTTPException(status_code=400, detail="Formato PREZZO nell'intervallo non valido: usare numeri")
                    if p1 > p2:
                        p1, p2 = p2, p1
                    condizioni.append(f"evento.COSTO BETWEEN %s AND %s")
                    valori.extend([p1, p2])

                # SINGOLO VALORE
                else:
                    # SINGOLO VALORE (es. PREZZO=>10)
                    m = re.match(r"^(<=|>=|<|>)\s*(\d+(?:\.\d+)?)$", PREZZO.strip())
                    if m:
                        operatore, valore = m.groups()
                        # Valida operatore con whitelist
                        cond = build_sql_condition("evento.COSTO", operatore, "COMPARAZIONE")
                        condizioni.append(cond)
                        valori.append(float(valore))
                    else:
                        # VALORE PLAIN (es. PREZZO=10)
                        plain = re.match(r"^(\d+(?:\.\d+)?)$", PREZZO.strip())
                        if plain:
                            valori.append(float(plain.group(1)))
                            condizioni.append("evento.COSTO = %s")
                        else:
                            raise HTTPException(status_code=400, detail="Formato PREZZO non valido: usa operatori <=, >=, <, > seguiti da un numero (es. >=10.5) oppure range min_max (es. 10_20)")

            # FILTRO CATEGORIA
            if CATEGORIA:
                condizioni.append("evento.ID_EVENTO IN (SELECT evento_categoria.ID_EVENTO FROM evento_categoria LEFT JOIN categoria ON evento_categoria.ID_CATEGORIA = categoria.ID_CATEGORIA WHERE categoria.NOME_CATEGORIA = %s)")
                valori.append(CATEGORIA)

            # FILTRO RICERCA
            if RICERCA:
                condizioni.append("LOWER(evento.NOME_EVENTO) LIKE %s")
                valori.append(f"%{RICERCA.lower()}%")

            # DISTANZA
            if DISTANZA:
                coordinate_sessione = request.session.get("COORDINATE")

                # SE NON PRESENTI COORDINATE
                if not coordinate_sessione:
                    raise HTTPException(status_code=400, detail="Coordinate non disponibili nella sessione utente")
                coordinate_db = normalizza_coordinate_input(coordinate_sessione)

                # RANGE MIN_MAX
                if "_" in DISTANZA:
                    parts = DISTANZA.split("_")
                    if len(parts) != 2:
                        raise HTTPException(status_code=400, detail="Intervallo DISTANZA non valido: usare 'min_max' (es. 1_5)")
                    try:
                        d1 = float(parts[0].strip())
                        d2 = float(parts[1].strip())
                    except ValueError:
                        raise HTTPException(status_code=400, detail="Formato DISTANZA nell'intervallo non valido: usare numeri (Km)")
                    if d1 > d2:
                        d1, d2 = d2, d1
                    valore_min = d1 * 1000
                    valore_max = d2 * 1000
                    condizioni.append(f"ST_Distance_Sphere(evento.COORDINATE_EVENTO, ST_GeomFromText(%s, 4326)) BETWEEN %s AND %s")
                    valori.append(coordinate_db)
                    valori.extend([valore_min, valore_max])
                    
                # SINGOLO VALORE
                else:
                    m = re.match(r"^(<=|>=|<|>)\s*(\d+(?:\.\d+)?)$", DISTANZA.strip())
                    # SINGOLO VALORE (es. DISTANZA=>5)
                    if m:
                        operatore, valore = m.groups()
                        valore_metri = float(valore) * 1000
                        # Valida operatore con whitelist
                        cond = build_sql_condition("ST_Distance_Sphere(evento.COORDINATE_EVENTO, ST_GeomFromText(%s, 4326))", operatore, "COMPARAZIONE")
                        condizioni.append(cond)
                        valori.append(coordinate_db)
                        valori.append(valore_metri)
                    else:
                        # VALORE PLAIN (es. DISTANZA=5)
                        plain = re.match(r"^(\d+(?:\.\d+)?)$", DISTANZA.strip())
                        if plain:
                            valore_metri = float(plain.group(1)) * 1000
                            condizioni.append("ST_Distance_Sphere(evento.COORDINATE_EVENTO, ST_GeomFromText(%s, 4326)) = %s")
                            valori.append(coordinate_db)
                            valori.append(valore_metri)
                        else:
                            raise HTTPException(status_code=400, detail="Formato DISTANZA non valido: usa operatori <=, >=, <, > seguiti da un numero (Km) o range min_max (es. 1_5) o valore plain (es. 5)")

            # QUERY FINALE
            where_clause = f"WHERE {' AND '.join(condizioni)}" if condizioni else ""
            query = f"""
                SELECT evento.ID_EVENTO, evento.NOME_EVENTO, evento.DESCRIZIONE_EVENTO, evento.DATA_EVENTO, evento.INDIRIZZO_EVENTO,
                       evento.COSTO, evento.CHECK_MAGGIORENNI, evento.MAX_PARTECIPANTI, evento.PASSWORD_EVENTO,
                       categoria.NOME_CATEGORIA AS CATEGORIA
                FROM evento
                {join_categoria}
                {where_clause}
                {order_clause}
            """
            cursor.execute(query, tuple(valori))
            eventi = cursor.fetchall()
            eventi = conversione(eventi)

            # RAGGRUPPA CATEGORIE PER EVENTO
            eventi_dict = {}
            for evento in eventi:
                evento_id = evento['ID_EVENTO']
                if evento_id not in eventi_dict:
                    evento_base = {k: v for k, v in evento.items() if k != 'CATEGORIA'}
                    evento_base['CATEGORIE'] = []
                    eventi_dict[evento_id] = evento_base
                
                if evento.get('CATEGORIA'):
                    if evento['CATEGORIA'] not in eventi_dict[evento_id]['CATEGORIE']:
                        eventi_dict[evento_id]['CATEGORIE'].append(evento['CATEGORIA'])
            
            eventi = list(eventi_dict.values())

            # RISPOSTA JSON
            return JSONResponse({
                "risultati": len(eventi),
                "eventi": eventi,
                "filtri": {
                    "ID_UTENTE": ID_UTENTE,
                    "ISCRITTO": ISCRITTO,
                    "MAGGIORENNI": MAGGIORENNI,
                    "HAS_PASSWORD": HAS_PASSWORD,
                    "DATA": DATA,
                    "ALFABETO": ALFABETO,
                    "PREZZO": PREZZO,
                    "CATEGORIA": CATEGORIA,
                    "DISTANZA": DISTANZA,
                    "RICERCA": RICERCA
                }
            })

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error retrieving events")
        raise HTTPException(status_code=500, detail="Errore interno")
    
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CATEGORIA SELEZIONATA (18) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /CATEGORIE/{ID_CATEGORIA}
@app.get("/CATEGORIE/{ID_CATEGORIA}")
async def get_categoria_selezionata(ID_CATEGORIA: int, request: Request):

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:

            # VERIFICA SESSIONE
            id_sessione = request.session.get("ID_UTENTE")

            # VERIFICA ADMIN
            _, is_admin = verifica_admin(id_sessione, cursor)       #   🡸 "_" Ignora "id_sessione"

            # QUERY CATEGORIA
            categoria = query_categoria(ID_CATEGORIA, cursor, full_data=is_admin)

            # SE NON TROVATO
            if not categoria:
                raise HTTPException(status_code=404, detail=f"Nessuna categoria con ID {ID_CATEGORIA} trovata")
            return JSONResponse(content=categoria)

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error retrieving category details")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CREA CATEGORIA (19) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# POST /CATEGORIE
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹
@app.post("/CATEGORIE")
async def crea_categoria(request: Request):

    # VERIFICA SESSIONE E PERMESSI ADMIN
    id_sessione = request.session.get("ID_UTENTE")
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")
    
    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)
            if not is_admin:
                raise HTTPException(status_code=403, detail="Permessi insufficienti")

            # DATI JSON
            data = await request.json()
            nome_categoria = normalizza_input_nullo(data.get("NOME_CATEGORIA"), tipo="str")
            if not nome_categoria:
                raise HTTPException(status_code=422, detail="NOME_CATEGORIA obbligatorio")

            # VERIFICA DUPLICATO
            cursor.execute("SELECT * FROM categoria WHERE NOME_CATEGORIA = %s", (nome_categoria,))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Categoria già esistente")

            # INSERIMENTO
            cursor.execute(
                "INSERT INTO categoria (NOME_CATEGORIA, ID_UTENTE) VALUES (%s, %s)",
                (nome_categoria, id_verificato)
            )
            connessione.commit()
            id_categoria = cursor.lastrowid

            # RISPOSTA JSON
            return JSONResponse({
                "message": "Categoria creata con successo",
                "ID_CATEGORIA": id_categoria,
                "NOME_CATEGORIA": nome_categoria,
                "ID_UTENTE": id_verificato
            })
    except mysql.connector.Error as err:
        logging.exception("Database error creating category")
        raise HTTPException(status_code=500, detail="Errore interno")
    
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| MODIFICA CATEGORIA (20) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# PUT /CATEGORIE/{ID_CATEGORIA}
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹
@app.put("/CATEGORIE/{ID_CATEGORIA}")
async def aggiorna_categoria(ID_CATEGORIA: int, request: Request):
    
    # VERIFICA SESSIONE E PERMESSI ADMIN
    id_sessione = request.session.get("ID_UTENTE")
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")
    
    # DATI JSON
    data = await request.json()
    nome_categoria = normalizza_input_nullo(data.get("NOME_CATEGORIA"), tipo="str")
    
    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)
            if not is_admin:
                raise HTTPException(status_code=403, detail="Permessi insufficienti")

            # VERIFICA CATEGORIA ESISTENTE
            cursor.execute("SELECT * FROM categoria WHERE ID_CATEGORIA = %s", (ID_CATEGORIA,))
            categoria = cursor.fetchone()
            if not categoria:
                raise HTTPException(status_code=404, detail="Categoria non trovata")

            # SE FORNITO NUOVO NOME
            if nome_categoria:

                # VERIFICA DUPLICATO
                cursor.execute("SELECT * FROM categoria WHERE NOME_CATEGORIA = %s AND ID_CATEGORIA != %s", 
                             (nome_categoria, ID_CATEGORIA))
                if cursor.fetchone():
                    raise HTTPException(status_code=409, detail="Categoria con questo nome già esistente")

                # AGGIORNAMENTO
                cursor.execute(
                    "UPDATE categoria SET NOME_CATEGORIA = %s WHERE ID_CATEGORIA = %s",
                    (nome_categoria, ID_CATEGORIA)
                )
                connessione.commit()

            # VERIFICA AGGIORNAMENTO
            cursor.execute("SELECT * FROM categoria WHERE ID_CATEGORIA = %s", (ID_CATEGORIA,))
            categoria_aggiornata = cursor.fetchone()

            # RISPOSTA JSON
            return JSONResponse({
                "message": "Categoria aggiornata con successo",
                "ID_CATEGORIA": categoria_aggiornata["ID_CATEGORIA"],
                "NOME_CATEGORIA": categoria_aggiornata["NOME_CATEGORIA"],
                "ID_UTENTE": categoria_aggiornata["ID_UTENTE"],
                "modificato_da": id_verificato
            })

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error updating category")
        raise HTTPException(status_code=500, detail="Errore interno")
    
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CANCELLA CATEGORIA (20) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# DELETE /CATEGORIE/{ID_CATEGORIA}
# 🡹 [⚠️GESTIONE PERMESSI ADMIN⚠️] 🡹
@app.delete("/CATEGORIE/{ID_CATEGORIA}")
async def elimina_categoria(ID_CATEGORIA: int, request: Request):
    
    # VERIFICA SESSIONE E PERMESSI ADMIN
    id_sessione = request.session.get("ID_UTENTE")
    if not id_sessione:
        raise HTTPException(status_code=401, detail="Utente non autenticato")
    
    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)
            if not is_admin:
                raise HTTPException(status_code=403, detail="Permessi insufficienti")

            # VERIFICA CATEGORIA ESISTENTE
            cursor.execute("SELECT * FROM categoria WHERE ID_CATEGORIA = %s", (ID_CATEGORIA,))
            categoria = cursor.fetchone()
            if not categoria:
                raise HTTPException(status_code=404, detail="Categoria non trovata")

            # ELIMINA CATEGORIA
            cursor.execute("DELETE FROM categoria WHERE ID_CATEGORIA = %s", (ID_CATEGORIA,))
            connessione.commit()

            # RISPOSTA JSON
            return JSONResponse({
                "message": "Categoria eliminata con successo",
                "ID_CATEGORIA": ID_CATEGORIA,
                "eliminato_da": id_verificato
            })

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error deleting category")
        raise HTTPException(status_code=500, detail="Errore interno")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#
# 🡹 file:///C%3A/Users/Sviatoslav/Desktop/ESAME%20WEB/BACKEND/BACKEND.PY#L240 🡹
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━| CATEGORIE FILTRATE (20) |━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━#

# GET /CATEGORIE?RICERCA=TESTO&ID_UTENTE=1
# ℹ️ ID_UTENTE = {ID_UTENTE}
# 🡹 [⚠️SOLO ADMIN POSSONO FILTRARE PER UTENTE⚠️] 🡹
# ℹ️ RICERCA = {...TESTO...}
@app.get("/CATEGORIE")
async def get_categorie(request: Request, RICERCA: Optional[str] = None, ID_UTENTE: Optional[int] = None):
    
    # VERIFICA SESSIONE (OPZIONALE - CONSENTI ACCESSO ANONIMO)
    id_sessione = request.session.get("ID_UTENTE")

    # NORMALIZZA PARAMETRI
    RICERCA = normalizza_input_nullo(RICERCA, tipo="str")

    # INIZIO
    try:
        with connessione.cursor(dictionary=True) as cursor:
            id_verificato, is_admin = verifica_admin(id_sessione, cursor)

            # FILTRO ID_UTENTE - SOLO ADMIN POSSONO FILTRARE PER UTENTE
            if ID_UTENTE and not is_admin:
                raise HTTPException(status_code=403, detail="Solo admin possono filtrare per ID_UTENTE")

            conditions = []
            values = []

            # FILTRO ID_UTENTE
            if ID_UTENTE:
                conditions.append("categoria.ID_UTENTE = %s")
                values.append(ID_UTENTE)

            # FILTRO RICERCA
            if RICERCA:
                 conditions.append("LOWER(categoria.NOME_CATEGORIA) LIKE %s")
                 values.append(f"%{RICERCA.lower()}%")

            # COSTRUZIONE QUERY
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            query = f"""
                SELECT ID_CATEGORIA, NOME_CATEGORIA, ID_UTENTE
                FROM categoria
                {where_clause}
                ORDER BY NOME_CATEGORIA ASC
            """

            # ESECUZIONE QUERY
            cursor.execute(query, tuple(values))
            categorie = cursor.fetchall()

            # RISPOSTA JSON
            return JSONResponse({
                "risultati": len(categorie),
                "categorie": categorie,
                "filtri": {
                    "RICERCA": RICERCA,
                    "ID_UTENTE": ID_UTENTE
                }
            })

    # ERRORE NELLA QUERY
    except mysql.connector.Error as err:
        logging.exception("Database error retrieving categories")
        raise HTTPException(status_code=500, detail="Errore interno")
