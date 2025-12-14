# BACKEND
python -m uvicorn BACKEND:app --reload

**(Frontend hardcoded per http localhost -> sconsigliato)**
python -m uvicorn BACKEND:app --reload --host 127.0.0.1 --port 8000 --ssl-keyfile="server.key" --ssl-certfile="server.crt"

# FRONTEND
ng new FRONTEND --routing --style=scss
ng generate component Home
ng serve

# GITHUB
[LINK_ORGINE]
https://github.com/WhileX1/ESAME-WEB
[SCARICA]
git clone https://github.com/WhileX1/ESAME-WEB.git