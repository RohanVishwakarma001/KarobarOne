"""add domain dns verification

Revision ID: 5bb5f9f357e0
Revises: d1cb39bfa6fb
Create Date: 2026-08-10
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5bb5f9f357e0"
down_revision: Union[str, Sequence[str], None] = "d1cb39bfa6fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tenantDomainMapping",
        sa.Column(
            "dnsVerified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "tenantDomainMapping",
        sa.Column(
            "dnsVerificationToken",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.alter_column(
        "tenantDomainMapping",
        "dnsVerified",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "tenantDomainMapping",
        "dnsVerificationToken",
    )

    op.drop_column(
        "tenantDomainMapping",
        "dnsVerified",
    )
