# TIENDAJ - Sistema de Gestión para Tienda de Videojuegos

Reescritura como aplicación web: API en FastAPI (Python) + frontend en React/TypeScript, con el mismo modelo de datos (18 tablas) de la versión original, ahora sobre Postgres.

## Arquitectura

```
backend/    API FastAPI + SQLAlchemy + Alembic (Postgres)
frontend/   React + TypeScript + Vite
infra/      docker-compose para desarrollo local
sql/        schema.sql original (SQL Server), como referencia del modelo de datos
```

## Desarrollo local

Con Docker (recomendado):

```bash
docker compose -f infra/docker-compose.yml up --build
docker compose -f infra/docker-compose.yml exec backend python -m app.seed  # datos de ejemplo
```

- Backend: http://localhost:8000 (docs interactivas en `/docs`)
- Frontend: http://localhost:5173

Sin Docker:

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload

# Frontend (usar pnpm, no npm)
cd frontend
pnpm install
pnpm dev
```

Usuario de ejemplo tras el seed: RFC `ISAA000101ABC`, contraseña `admin123`.

## Tests y lint

```bash
cd backend && ruff check app tests && pytest
cd frontend && pnpm exec oxlint && pnpm exec tsc -b
```

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) corre lint + tests + build de imágenes en cada PR. El despliegue a un VPS vía Docker Compose está en progreso.

## Funcionalidades

- Login de empleados (JWT)
- Dashboard con métricas (videojuegos, clientes, ventas, ingresos)
- Catálogo de videojuegos (alta/baja)
- Clientes (alta/baja)
- Registro de ventas con descuento automático de inventario

## Historial

Este proyecto empezó como una app de escritorio en CustomTkinter + SQL Server. Esa versión y su equivalente web en Flask/MariaDB se pueden consultar en el historial de git antes del commit "Fase 1: eliminar apps legacy...".
