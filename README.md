# BACKEND
python -m uvicorn BACKEND:app --reload

python -m uvicorn BACKEND:app --reload --host 127.0.0.1 --port 8000 --ssl-keyfile="server.key" --ssl-certfile="server.crt"

# FRONTEND
ng new FRONTEND --routing --style=scss
ng generate component Home
ng serve

# GITHUB
[COLLEGA_GITHUB]
git init
[LINK_ORGINE]
git remote add origin https://github.com/WhileX1/ESAME-WEB

# PROVA ANCORA