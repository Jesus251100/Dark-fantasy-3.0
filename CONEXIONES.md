# Conexiones Dark Fantasy 3.0

```
Navegador  →  http://127.0.0.1:5173
                ↓
FRONTEND (Vue, nginx en Docker: darkfantasy-web)
  /api/... se reenvía al backend
                ↓
BACKEND (Express, Docker: darkfantasy-api :3001)
                ↓
PostgreSQL (Docker: darkfantasy-pg, host 5433 → contenedor 5432)
```

## Arranque con Docker (recomendado)

En la carpeta del proyecto:

```
cd C:\Users\sanch\Downloads\Dark-fantasy-3.0
docker compose up --build
```

La primera vez tarda unos minutos (instala Node y construye el juego).
Cuando termine, abre: **http://127.0.0.1:5173**

Usuarios de prueba:

- Jugador: `jugador@darkfantasy.com` / `jugador123`
- Admin: `admin@darkfantasy.com` / `admin123`

Registro: el código llega al correo real del jugador (Gmail, Outlook, etc.) si en `.env` están `SMTP_USER` y `SMTP_PASS` (contraseña de aplicación de Gmail, no la clave de la cuenta):

```
SMTP_USER=tucorreo@gmail.com
SMTP_PASS=xxxx xxxx xxxx xxxx
SMTP_FROM=Dark Fantasy <tucorreo@gmail.com>
```

Sin esas variables, el código queda en Mailpit: **http://127.0.0.1:8025**

Si el puerto 5173 o 3001 ya está ocupado (un `npm run dev` viejo), ciérralo y vuelve a lanzar Compose.

Si Compose se queja de la red o el API sale con código 137:

```
docker compose down
docker compose up -d --build
```

El juego es **http://127.0.0.1:5173** (no el 3001). El 3001 es solo el API.

Parar:

```
docker compose down
```

## Arranque local (sin el front/API en Docker)

Postgres sigue en Docker:

```
docker start darkfantasy-pg
```

Backend:

```
cd backend
npm run dev
```

Frontend (otra terminal):

```
cd Dark-fantasy-3.0
npm run dev
```

## pgAdmin

Servidor NUEVO, no el de puerto 5432:

- Host: `127.0.0.1`
- Puerto: `5433`
- Database: `darkfantasy`
- User / Password: `darkfantasy` / `darkfantasy`
