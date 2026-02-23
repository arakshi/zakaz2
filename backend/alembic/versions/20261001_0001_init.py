"""init schema

Revision ID: 20261001_0001
Revises:
Create Date: 2026-10-01 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20261001_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "raw_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("event_time", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_raw_events_source", "raw_events", ["source"])
    op.create_index("ix_raw_events_event_time", "raw_events", ["event_time"])

    op.create_table(
        "marketing_daily_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("metric_date", sa.Date(), nullable=False),
        sa.Column("channel", sa.String(length=80), nullable=False),
        sa.Column("campaign", sa.String(length=120), nullable=False),
        sa.Column("device", sa.String(length=50), nullable=False),
        sa.Column("region", sa.String(length=80), nullable=False),
        sa.Column("visits", sa.Integer(), nullable=False),
        sa.Column("orders", sa.Integer(), nullable=False),
        sa.Column("revenue", sa.Float(), nullable=False),
        sa.Column("cost", sa.Float(), nullable=False),
        sa.Column("users_new", sa.Integer(), nullable=False),
        sa.Column("users_returning", sa.Integer(), nullable=False),
        sa.UniqueConstraint("metric_date", "channel", "campaign", name="uq_metric_day_channel_campaign"),
    )
    op.create_index("ix_mkt_metric_date", "marketing_daily_metrics", ["metric_date"])
    op.create_index("ix_mkt_channel", "marketing_daily_metrics", ["channel"])
    op.create_index("ix_mkt_campaign", "marketing_daily_metrics", ["campaign"])

    op.create_table(
        "report_templates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "generated_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("template_id", sa.Integer(), sa.ForeignKey("report_templates.id"), nullable=False),
        sa.Column("period_from", sa.Date(), nullable=False),
        sa.Column("period_to", sa.Date(), nullable=False),
        sa.Column("html_content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("generated_reports")
    op.drop_table("report_templates")
    op.drop_index("ix_mkt_campaign", table_name="marketing_daily_metrics")
    op.drop_index("ix_mkt_channel", table_name="marketing_daily_metrics")
    op.drop_index("ix_mkt_metric_date", table_name="marketing_daily_metrics")
    op.drop_table("marketing_daily_metrics")
    op.drop_index("ix_raw_events_event_time", table_name="raw_events")
    op.drop_index("ix_raw_events_source", table_name="raw_events")
    op.drop_table("raw_events")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
