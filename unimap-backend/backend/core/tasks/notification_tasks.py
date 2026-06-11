"""
UniMap 3.0 - Celery Notification Tasks
Async notification delivery: email, push, in-app
"""
import structlog
from celery import shared_task

logger = structlog.get_logger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name="backend.core.tasks.notification_tasks.send_notification",
)
def send_notification(self, recipient_id: str, title: str, body: str, channels: list[str]):
    """
    Deliver a notification via configured channels.
    Channels: in_app | email | push
    """
    try:
        if "email" in channels:
            _send_email_notification(recipient_id, title, body)
        if "push" in channels:
            _send_push_notification(recipient_id, title, body)
        logger.info("notification_sent", recipient=recipient_id, channels=channels)
    except Exception as exc:
        logger.error("notification_failed", error=str(exc))
        raise self.retry(exc=exc)


@shared_task(name="backend.core.tasks.notification_tasks.send_deadline_reminders")
def send_deadline_reminders():
    """
    Notify students of academic deadlines due within 24h.
    Scheduled daily via Celery Beat.
    """
    from backend.shared.database.engine import get_db_context
    import asyncio

    async def _run():
        async with get_db_context() as session:
            from sqlalchemy import select
            from backend.api.modules.agenda.models.agenda_models import Activity
            from datetime import datetime, timezone, timedelta

            now = datetime.now(timezone.utc)
            due_soon = now + timedelta(hours=24)

            stmt = select(Activity).where(
                Activity.due_at >= now,
                Activity.due_at <= due_soon,
                Activity.is_completed == False,
                Activity.deleted_at.is_(None),
            )
            result = await session.execute(stmt)
            activities = result.scalars().all()

            logger.info("deadline_reminder_task", count=len(activities))
            # TODO: Queue individual notifications per student
            return len(activities)

    return asyncio.get_event_loop().run_until_complete(_run())


def _send_email_notification(recipient_id: str, title: str, body: str):
    """
    Send email via SMTP.
    TODO: integrate with email provider (SendGrid, AWS SES, etc.)
    """
    logger.info("email_queued", recipient=recipient_id, subject=title)


def _send_push_notification(recipient_id: str, title: str, body: str):
    """
    Send push notification via FCM/APNs.
    TODO: integrate with Firebase Cloud Messaging
    """
    logger.info("push_queued", recipient=recipient_id, title=title)
