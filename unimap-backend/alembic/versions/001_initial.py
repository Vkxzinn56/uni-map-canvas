"""Initial schema — UniMap 3.0

Revision ID: 001_initial
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── users ──────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.Text, nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(100)),
        sa.Column("avatar_url", sa.Text),
        sa.Column("phone", sa.String(20)),
        sa.Column("role", sa.String(50), nullable=False, server_default="visitor"),
        sa.Column("cpf_encrypted", sa.Text),
        sa.Column("cpf_hash", sa.String(64), unique=True),
        sa.Column("address_encrypted", sa.Text),
        sa.Column("is_verified", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_blocked", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("block_reason", sa.Text),
        sa.Column("lgpd_consent_at", sa.DateTime(timezone=True)),
        sa.Column("lgpd_consent_ip", sa.String(45)),
        sa.Column("anonymized_at", sa.DateTime(timezone=True)),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
        sa.Column("last_login_ip", sa.String(45)),
        sa.Column("failed_login_attempts", sa.Integer, nullable=False, server_default="0"),
        sa.Column("locked_until", sa.DateTime(timezone=True)),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_role", "users", ["role"])
    op.create_index("ix_users_cpf_hash", "users", ["cpf_hash"])

    # ── students ───────────────────────────────────────────────────────────────
    op.create_table(
        "students",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), unique=True, nullable=False),
        sa.Column("rgm_encrypted", sa.Text, nullable=False),
        sa.Column("rgm_hash", sa.String(64), unique=True, nullable=False),
        sa.Column("course", sa.String(200), nullable=False),
        sa.Column("course_code", sa.String(20)),
        sa.Column("semester", sa.Integer, nullable=False, server_default="1"),
        sa.Column("enrollment_year", sa.Integer, nullable=False),
        sa.Column("expected_graduation", sa.Date),
        sa.Column("graduation_date", sa.Date),
        sa.Column("campus", sa.String(100), nullable=False),
        sa.Column("campus_code", sa.String(10)),
        sa.Column("period", sa.String(10), nullable=False, server_default="morning"),
        sa.Column("enrollment_status", sa.String(30), nullable=False, server_default="active"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── map_blocks ─────────────────────────────────────────────────────────────
    op.create_table(
        "map_blocks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(20), unique=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("short_name", sa.String(50)),
        sa.Column("block_type", sa.String(50), nullable=False, server_default="academic"),
        sa.Column("description", sa.Text),
        sa.Column("floor_count", sa.Integer, nullable=False, server_default="1"),
        sa.Column("image_url", sa.Text),
        sa.Column("latitude", sa.Float),
        sa.Column("longitude", sa.Float),
        sa.Column("geojson", JSON),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── map_rooms ──────────────────────────────────────────────────────────────
    op.create_table(
        "map_rooms",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("block_id", UUID(as_uuid=True), sa.ForeignKey("map_blocks.id"), nullable=False),
        sa.Column("code", sa.String(30), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("floor", sa.Integer, nullable=False, server_default="0"),
        sa.Column("capacity", sa.Integer),
        sa.Column("room_type", sa.String(50), nullable=False, server_default="classroom"),
        sa.Column("amenities", JSON),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── map_routes ─────────────────────────────────────────────────────────────
    op.create_table(
        "map_routes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("origin_block_id", UUID(as_uuid=True), sa.ForeignKey("map_blocks.id")),
        sa.Column("destination_block_id", UUID(as_uuid=True), sa.ForeignKey("map_blocks.id")),
        sa.Column("origin_label", sa.String(200), nullable=False),
        sa.Column("destination_label", sa.String(200), nullable=False),
        sa.Column("distance_meters", sa.Float),
        sa.Column("duration_minutes", sa.Float),
        sa.Column("is_accessible", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("waypoints", JSON),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── events ─────────────────────────────────────────────────────────────────
    op.create_table(
        "events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("short_description", sa.String(500)),
        sa.Column("category", sa.String(50), nullable=False, server_default="general"),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location_name", sa.String(200)),
        sa.Column("block_id", UUID(as_uuid=True), sa.ForeignKey("map_blocks.id")),
        sa.Column("room_id", UUID(as_uuid=True), sa.ForeignKey("map_rooms.id")),
        sa.Column("image_url", sa.Text),
        sa.Column("external_link", sa.Text),
        sa.Column("organizer_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("organizer_name", sa.String(200)),
        sa.Column("max_capacity", sa.Integer),
        sa.Column("registration_required", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("registration_url", sa.Text),
        sa.Column("status", sa.String(20), nullable=False, server_default="published"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── academic_classes ───────────────────────────────────────────────────────
    op.create_table(
        "academic_classes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("subject_code", sa.String(30), nullable=False),
        sa.Column("subject_name", sa.String(200), nullable=False),
        sa.Column("professor_name", sa.String(200)),
        sa.Column("day_of_week", sa.Integer, nullable=False),
        sa.Column("start_time", sa.Time, nullable=False),
        sa.Column("end_time", sa.Time, nullable=False),
        sa.Column("block_code", sa.String(20)),
        sa.Column("room_code", sa.String(30)),
        sa.Column("semester_label", sa.String(20), nullable=False),
        sa.Column("class_type", sa.String(20), nullable=False, server_default="theoretical"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── activities ─────────────────────────────────────────────────────────────
    op.create_table(
        "activities",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.String(1000)),
        sa.Column("activity_type", sa.String(30), nullable=False),
        sa.Column("subject_code", sa.String(30)),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_completed", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("weight", sa.Float),
        sa.Column("max_score", sa.Float),
        sa.Column("achieved_score", sa.Float),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── clinics ────────────────────────────────────────────────────────────────
    op.create_table(
        "clinics",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("clinic_type", sa.String(50), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("location", sa.String(200)),
        sa.Column("block_code", sa.String(20)),
        sa.Column("room_code", sa.String(30)),
        sa.Column("phone", sa.String(20)),
        sa.Column("email", sa.String(255)),
        sa.Column("schedule_info", sa.Text),
        sa.Column("image_url", sa.Text),
        sa.Column("accepts_walk_in", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── clinic_appointments ────────────────────────────────────────────────────
    op.create_table(
        "clinic_appointments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("patient_user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("duration_minutes", sa.Integer, nullable=False, server_default="30"),
        sa.Column("appointment_type", sa.String(50), nullable=False),
        sa.Column("notes", sa.Text),
        sa.Column("status", sa.String(20), nullable=False, server_default="scheduled"),
        sa.Column("cancellation_reason", sa.Text),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── clinic_budgets ─────────────────────────────────────────────────────────
    op.create_table(
        "clinic_budgets",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("clinic_id", UUID(as_uuid=True), sa.ForeignKey("clinics.id"), nullable=False),
        sa.Column("patient_user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("appointment_id", UUID(as_uuid=True), sa.ForeignKey("clinic_appointments.id")),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("procedures", sa.Text),
        sa.Column("estimated_sessions", sa.Integer),
        sa.Column("valid_until", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── notifications ──────────────────────────────────────────────────────────
    op.create_table(
        "notifications",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("recipient_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("notification_type", sa.String(50), nullable=False),
        sa.Column("reference_type", sa.String(50)),
        sa.Column("reference_id", sa.String(36)),
        sa.Column("is_read", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("read_at", sa.DateTime(timezone=True)),
        sa.Column("sender_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("channels", JSON),
        sa.Column("metadata", JSON),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True)),
    )

    # ── audit_logs ─────────────────────────────────────────────────────────────
    op.create_table(
        "audit_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor_id", sa.String(36)),
        sa.Column("actor_role", sa.String(50)),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(36)),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("user_agent", sa.Text),
        sa.Column("metadata", JSON),
        sa.Column("request_id", sa.String(36)),
        sa.Column("success", sa.Boolean, nullable=False, server_default="true"),
    )
    op.create_index("ix_audit_logs_timestamp", "audit_logs", ["timestamp"])
    op.create_index("ix_audit_logs_actor_id", "audit_logs", ["actor_id"])
    op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_index("ix_audit_logs_resource_type", "audit_logs", ["resource_type"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("notifications")
    op.drop_table("clinic_budgets")
    op.drop_table("clinic_appointments")
    op.drop_table("clinics")
    op.drop_table("activities")
    op.drop_table("academic_classes")
    op.drop_table("events")
    op.drop_table("map_routes")
    op.drop_table("map_rooms")
    op.drop_table("map_blocks")
    op.drop_table("students")
    op.drop_table("users")
