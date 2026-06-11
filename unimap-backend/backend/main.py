"""
UniMap 3.0 - Application Factory
Main FastAPI entry point — Clean Architecture composition root
"""
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from prometheus_client import make_asgi_app
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from backend.core.config.settings import settings
from backend.shared.database.engine import engine
from backend.shared.middleware.handlers import setup_exception_handlers, setup_middleware

# ─── Routers ──────────────────────────────────────────────────────────────────
from backend.api.modules.auth.router.auth_router import router as auth_router
from backend.api.modules.users.router.user_router import router as users_router
from backend.api.modules.maps.router.map_router import router as maps_router
from backend.api.modules.events.router.event_router import router as events_router
from backend.api.modules.agenda.router.agenda_router import router as agenda_router
from backend.api.modules.clinics.router.clinic_router import router as clinics_router
from backend.api.modules.notifications.router.notification_router import router as notifications_router
from backend.api.modules.audit.router.audit_router import router as audit_router
from backend.api.modules.analytics.router.analytics_router import router as analytics_router

logger = structlog.get_logger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle hooks."""
    logger.info("unimap_startup", version=settings.APP_VERSION, env=settings.APP_ENV)

    # Validate DB connection
    try:
        async with engine.connect() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        logger.info("database_connected")
    except Exception as e:
        logger.error("database_connection_failed", error=str(e))
        raise

    # Validate Redis connection
    try:
        from backend.shared.cache.redis_service import get_redis_pool
        redis = await get_redis_pool()
        await redis.ping()
        logger.info("redis_connected")
    except Exception as e:
        logger.warning("redis_connection_failed", error=str(e))

    yield

    logger.info("unimap_shutdown")
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="UniMap API",
        description="""
## UniMap 3.0 Backend API

Corporate university campus management system.

### Features
- 🗺️ **Campus Map** — Interactive blocks, rooms, and routing
- 📅 **Agenda** — Class schedules and academic activities (STUDENT+)
- 🏥 **Clinics** — University health/dental clinic booking
- 📢 **Events** — Campus event listing and management
- 🔔 **Notifications** — In-app notification system
- 🔐 **RBAC** — Role-based access: Visitor → Admin
- 🛡️ **LGPD** — Brazilian data protection compliance
- 📊 **Analytics** — Platform usage metrics
- 📋 **Audit** — Full compliance audit trail

### Authentication
All protected endpoints use **JWT Bearer** tokens.
Obtain tokens via `POST /api/v1/auth/login`.
        """,
        version=settings.APP_VERSION,
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        contact={
            "name": "UniMap Team",
            "email": "dev@unimap.edu.br",
        },
        license_info={
            "name": "Proprietary",
        },
    )

    # ─── Rate Limiter ─────────────────────────────────────────────────────────
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ─── Middleware ────────────────────────────────────────────────────────────
    setup_middleware(app)
    setup_exception_handlers(app)

    # ─── Routers ──────────────────────────────────────────────────────────────
    prefix = settings.API_PREFIX
    app.include_router(auth_router, prefix=prefix)
    app.include_router(users_router, prefix=prefix)
    app.include_router(maps_router, prefix=prefix)
    app.include_router(events_router, prefix=prefix)
    app.include_router(agenda_router, prefix=prefix)
    app.include_router(clinics_router, prefix=prefix)
    app.include_router(notifications_router, prefix=prefix)
    app.include_router(audit_router, prefix=prefix)
    app.include_router(analytics_router, prefix=prefix)

    # ─── Health Check ─────────────────────────────────────────────────────────
    @app.get("/health", tags=["Health"], include_in_schema=False)
    async def health():
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
        }

    @app.get("/ready", tags=["Health"], include_in_schema=False)
    async def readiness():
        """Kubernetes readiness probe."""
        checks = {}
        # DB check
        try:
            async with engine.connect() as conn:
                from sqlalchemy import text
                await conn.execute(text("SELECT 1"))
            checks["database"] = "ok"
        except Exception:
            checks["database"] = "error"

        # Redis check
        try:
            from backend.shared.cache.redis_service import get_redis_pool
            redis = await get_redis_pool()
            await redis.ping()
            checks["redis"] = "ok"
        except Exception:
            checks["redis"] = "error"

        all_ok = all(v == "ok" for v in checks.values())
        return ORJSONResponse(
            status_code=200 if all_ok else 503,
            content={"status": "ready" if all_ok else "degraded", "checks": checks},
        )

    # ─── Prometheus metrics ───────────────────────────────────────────────────
    if settings.PROMETHEUS_ENABLED:
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)

    return app


app = create_app()
