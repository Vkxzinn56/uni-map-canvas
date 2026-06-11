# UniMap 3.0 — Backend API

Backend corporativo do sistema de mapeamento universitário UniMap.

## Stack

- **Python 3.11** + **FastAPI** — API principal
- **PostgreSQL 16** + **SQLAlchemy 2 (async)** — banco de dados
- **Redis 7** — cache e filas
- **Argon2** — hashing de senhas
- **AES-256-GCM** — criptografia de campos sensíveis (CPF, RGM, endereço)
- **JWT** (access + refresh) — autenticação
- **Celery** — tarefas assíncronas
- **Alembic** — migrações
- **Docker + Docker Compose** — ambiente

## Arquitetura

Clean Architecture + DDD + SOLID + Repository Pattern

```
backend/
├── api/modules/          # Módulos de domínio
│   ├── auth/             # Autenticação JWT + RBAC
│   ├── users/            # Gestão de usuários
│   ├── students/         # Perfil acadêmico
│   ├── maps/             # Mapa do campus
│   ├── events/           # Eventos
│   ├── agenda/           # Agenda acadêmica (STUDENT+)
│   ├── clinics/          # Clínicas universitárias
│   ├── notifications/    # Notificações in-app
│   ├── blackboard/       # Integração Blackboard (preparada)
│   ├── analytics/        # Métricas da plataforma
│   └── audit/            # Logs de auditoria LGPD
├── core/                 # Config, Celery, tarefas
└── shared/               # DB, cache, segurança, middlewares
```

## Perfis de Acesso (RBAC)

| Role | Mapa | Clínicas | Eventos | Agenda | Acadêmico | Admin |
|------|------|----------|---------|--------|-----------|-------|
| Visitante | ✅ | 👁️ | 👁️ | ❌ | ❌ | ❌ |
| Aluno | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Professor | ✅ | ✅ | ✅✏️ | ✅✏️ | ✅ | ❌ |
| Coordenação | ✅ | ✅✏️ | ✅✏️ | ✅✏️ | ✅ | parcial |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Alumni | ✅ | 👁️ | 👁️ | ❌ | histórico | ❌ |

## Início Rápido

```bash
# 1. Clone e configure
cp .env.example .env
# edite .env com suas chaves

# 2. Suba os serviços
docker compose up -d

# 3. Rode as migrações
docker compose exec api alembic upgrade head

# 4. Popule o banco (dev)
docker compose exec api python scripts/seed_db.py

# 5. Acesse a documentação
open http://localhost:8000/api/v1/docs
```

## Contas de teste (após seed)

| Conta | Email | Senha |
|-------|-------|-------|
| Admin | admin@unimap.edu.br | AdminPass123! |
| Aluno | aluno@unimap.edu.br | AlunoPass123! |
| Visitante | visitante@unimap.edu.br | VisitPass123! |

## Testes

```bash
# Rodar todos os testes (≥90% cobertura exigida)
pytest

# Com relatório de cobertura HTML
pytest --cov-report=html
open htmlcov/index.html
```

## Variáveis de Ambiente obrigatórias

| Variável | Descrição |
|----------|-----------|
| `SECRET_KEY` | Chave secreta da app (min 32 chars) |
| `JWT_SECRET_KEY` | Chave JWT (min 32 chars) |
| `ENCRYPTION_KEY` | Chave AES-256 (min 32 chars) |
| `DATABASE_URL` | PostgreSQL async URL |
| `REDIS_URL` | Redis URL |

## CI/CD

GitHub Actions — `.github/workflows/ci-cd.yml`

- **lint** → Ruff + Black + MyPy
- **test** → Pytest ≥90% cobertura
- **security** → Bandit + Safety
- **build** → Docker image → GHCR
- **deploy** → staging (develop) / production (main)

## Blackboard

A integração com o Blackboard está **preparada mas não ativa**.  
Para ativar: `BLACKBOARD_ENABLED=true` no `.env` e implemente `RealBlackboardAdapter`.

## LGPD

- Soft delete em todos os registros
- Anonimização automática após período de retenção (Celery Beat)
- Criptografia AES-256-GCM para CPF, RGM e endereço
- Log de auditoria completo de todas as operações
- Endpoint de exclusão de conta (`DELETE /api/v1/users/me`)
