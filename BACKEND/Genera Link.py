import os
import urllib.parse

# PERSONALIZZA IL PATH
path = "C:/Users/Sviatoslav/Desktop/ESAME WEB/BACKEND/BACKEND.PY"
encoded_path = urllib.parse.quote(path)

# RIGHE API
lines = [457, 485, 714, 745, 833, 
         846, 890, 985, 
         1144, 1287, 1349, 
         1392, 1507, 1621, 
         1680, 1778, 1826, 
         1996, 2159, 2203, 
         2283, 2522, 2553, 
         2604, 2669, 2712]

names = [
    "CLASSI","FUNZIONI","SESSIONE","LOGIN","LOGOUT",
    "DETTAGLI UTENTE","FILTRO_UTENTI","REGISTRAZIONE",
    "MODIFICA UTENTE", "ELIMINA UTENTE", "DETTAGLI ISCRIZIONE",
    "FILTRO ISCRIZIONI", "CREA ISCRIZIONE", "CANCELLA ISCRIZIONE",
    "CANCELLA ISCRIZIONI FILTRATE", "EVENTO SELEZIONATO", "CREA EVENTO",
    "MODIFICA EVENTO", "CANCELLA EVENTO", "CANCELLA EVENTI FILTRATI",
    "EVENTI FILTRATI", "CATEGORIA SELEZIONATA", "CREA CATEGORIA",
    "MODIFICA CATEGORIA", "CANCELLA CATEGORIA", "CATEGORIE FILTRATE"
         ]

os.system("cls")
print("🔗 LISTA API:\n", flush=True)

# GENERA LINK
for i, line in enumerate(lines):
    link = f"# file:///{encoded_path}#L{line}"
    print(link + "   " + f"━|{names[i]}|━", flush=True)

# RIGA MENU RAPIDO
lines = [240]
names = ["BACK"]

print ()
print("🔗 MENU:\n", flush=True)

# GENERA LINK
for i, line in enumerate(lines):
    link = f"file:///{encoded_path}#L{line}"
    print("# 🡹 "+link+" 🡹", flush=True)
    print()


