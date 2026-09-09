# Infra — desarrollo local

```bash
cp ../backend/.env.example ../backend/.env      # opcional, docker-compose ya trae defaults de dev
docker compose -f docker-compose.yml up --build
```

Levanta:
- `db`: Postgres 16
- `backend`: FastAPI en `http://localhost:8000` (corre las migraciones de Alembic al iniciar)
- `frontend`: Vite dev server con hot-reload en `http://localhost:5173`

Para sembrar datos de ejemplo una vez que el backend esté arriba:

```bash
docker compose exec backend python -m app.seed
```
