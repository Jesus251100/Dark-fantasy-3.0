# Backend Dark Fantasy (POO + SOLID + PostgreSQL)

API en TypeScript. Las reglas de campaña/tienda son las mismas clases del front (`Campania`, `Jugador`, `ComprarBooster`).

## Cómo arrancar

### Todo el juego con Docker (recomendado)

Desde la carpeta raíz del proyecto (`Dark-fantasy-3.0`):

```
docker compose up --build
```

Juego: http://127.0.0.1:5173  
API:    http://127.0.0.1:3001/api/salud

### Solo este backend en local

1. PostgreSQL (Docker, puerto 5433):

```
docker start darkfantasy-pg
```

Si no existe el contenedor:

```
docker run -d --name darkfantasy-pg -e POSTGRES_USER=darkfantasy -e POSTGRES_PASSWORD=darkfantasy -e POSTGRES_DB=darkfantasy -p 5433:5432 postgres:16-alpine
```

2. En esta carpeta:

```
npm install
npx prisma db push
npx tsx prisma/seed.ts
npm run dev
```

API: http://127.0.0.1:3001

## Usuarios de prueba

- Jugador: `jugador@darkfantasy.com` / `jugador123` (también vale `jugador@darkfantasy.local`)
- Admin: `admin@darkfantasy.com` / `admin123` (también vale `admin@darkfantasy.local`)

## Rutas

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/campania`
- `POST /api/campania/completar-nivel`
- `POST /api/campania/comprar-booster`
- `POST /api/campania/intercambiar`
- `GET /api/admin/usuarios` (solo admin)
- `GET /api/admin/reportes` (solo admin)
