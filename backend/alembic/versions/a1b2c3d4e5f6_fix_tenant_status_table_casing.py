"""fix tenantStatus table/column casing to match the TenantStatus model

Same root cause as f1a2b3c4d5e6: this table was created (in df84845c699e)
as 'tenantStatus' with camelCase columns, but the TenantStatus model
expects table 'tenant_status' with snake_case columns. This has made
every status lookup fail outright (UndefinedTableError) rather than
gracefully return no rows.

Revision ID: a1b2c3d4e5f6
Revises: f1a2b3c4d5e6
Create Date: 2026-08-28 15:15:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'f1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

RENAMES = [
    ("statusName", "status_name"),
    ("statusDescription", "status_description"),
    ("createdAt", "created_at"),
]


def upgrade() -> None:
    op.rename_table("tenantStatus", "tenant_status")
    for old_name, new_name in RENAMES:
        op.alter_column("tenant_status", old_name, new_column_name=new_name)


def downgrade() -> None:
    for old_name, new_name in RENAMES:
        op.alter_column("tenant_status", new_name, new_column_name=old_name)
    op.rename_table("tenant_status", "tenantStatus")
