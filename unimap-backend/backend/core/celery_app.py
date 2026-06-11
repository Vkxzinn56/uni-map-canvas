"""
UniMap 3.0 - Celery Application
Task queue for async jobs: notifications, sync, reports
"""
from celery import Celery
from backend.core.config.settings import settings

celery_app = Celery(
    "unimap",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "backend.core.tasks.notification_tasks",
        "backend.core.tasks.maintenance_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        # Run LGPD data retention cleanup daily at 02:00
        "lgpd-cleanup": {
            "task": "backend.core.tasks.maintenance_tasks.lgpd_cleanup",
            "schedule": 86400,  # every 24 hours
        },
        # Notify students of upcoming deadlines every morning at 07:00
        "deadline-reminders": {
            "task": "backend.core.tasks.notification_tasks.send_deadline_reminders",
            "schedule": 86400,
        },
    },
)
