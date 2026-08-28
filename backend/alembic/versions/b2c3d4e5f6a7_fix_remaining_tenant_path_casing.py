"""fix remaining casing bugs on the tenant/store creation path, add missing tenant_settings

Same root cause as f1a2b3c4d5e6/a1b2c3d4e5f6 (df84845c699e authored several
tables/columns in camelCase instead of the snake_case the models expect).
This migration covers the remaining tables that sit on the tenant + store
creation path:
  - tenantDomainMapping -> tenant_domain_mapping (+ column casing)
  - tenantPlanMapping   -> tenant_plan_mapping (+ column casing)
  - userRoleMapping     -> user_role_mapping (columns already snake_case)
  - tenant_settings: never created by any prior migration under any name;
    created here from scratch to match the TenantSettings model exactly.

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-28 15:45:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DOMAIN_MAPPING_RENAMES = [
    ("tenantId", "tenant_id"),
    ("domainType", "domain_type"),
    ("subDomain", "sub_domain"),
    ("customDomain", "custom_domain"),
    ("isPrimary", "is_primary"),
    ("dnsVerified", "dns_verified"),
    ("dnsVerificationToken", "dns_verification_token"),
    ("sslExpiry", "ssl_expiry"),
]

PLAN_MAPPING_RENAMES = [
    ("tenantId", "tenant_id"),
    ("planId", "plan_id"),
    ("planStartDate", "plan_start_date"),
    ("planEndDate", "plan_end_date"),
    ("planUpdateAt", "plan_update_at"),
    ("autoRenew", "auto_renew"),
    ("planChange", "plan_change"),
    ("changeReason", "change_reason"),
    ("statusId", "status_id"),
    ("statusUpdateAt", "status_update_at"),
    ("statusUpdateBy", "status_update_by"),
]


def upgrade() -> None:
    op.rename_table("tenantDomainMapping", "tenant_domain_mapping")
    for old_name, new_name in DOMAIN_MAPPING_RENAMES:
        op.alter_column("tenant_domain_mapping", old_name, new_column_name=new_name)

    op.rename_table("tenantPlanMapping", "tenant_plan_mapping")
    for old_name, new_name in PLAN_MAPPING_RENAMES:
        op.alter_column("tenant_plan_mapping", old_name, new_column_name=new_name)

    op.rename_table("userRoleMapping", "user_role_mapping")

    op.create_table(
        "tenant_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tenantId", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("currency", sa.String(length=10), server_default="INR", nullable=False),
        sa.Column("timezone", sa.String(length=50), server_default="Asia/Kolkata", nullable=False),
        sa.Column("language", sa.String(length=10), server_default="en", nullable=False),
        sa.Column("invoicePrefix", sa.String(length=50), nullable=True),
        sa.Column("fiscalYearStart", sa.Integer(), server_default="4", nullable=False),
        sa.Column("taxRate", sa.Numeric(5, 2), server_default="0.00", nullable=False),
        sa.Column("enableNotifications", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("enableAutoRenew", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenantId"], ["tenants_details.id"], ondelete="CASCADE", name=op.f("fk_tenant_settings_tenantId_tenants_details")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tenant_settings")),
        sa.UniqueConstraint("tenantId", name=op.f("uq_tenant_settings_tenantId")),
    )


def downgrade() -> None:
    op.drop_table("tenant_settings")

    op.rename_table("user_role_mapping", "userRoleMapping")

    for old_name, new_name in PLAN_MAPPING_RENAMES:
        op.alter_column("tenant_plan_mapping", new_name, new_column_name=old_name)
    op.rename_table("tenant_plan_mapping", "tenantPlanMapping")

    for old_name, new_name in DOMAIN_MAPPING_RENAMES:
        op.alter_column("tenant_domain_mapping", new_name, new_column_name=old_name)
    op.rename_table("tenant_domain_mapping", "tenantDomainMapping")
