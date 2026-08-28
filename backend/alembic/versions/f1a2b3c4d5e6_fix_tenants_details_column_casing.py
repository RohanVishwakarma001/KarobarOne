"""fix tenants_details column casing to match the Tenant model

The tenants_details table was created (in df84845c699e) with camelCase
column names (gstNumber, panNumber, businessName, ...), but the Tenant
SQLAlchemy model maps every field to a snake_case column name
(gst_number, pan_number, business_name, ...). Every read/write against
this table has been broken since — this migration renames the columns
to match what the model actually expects. Postgres automatically
updates dependent objects (check constraints, indexes) on column rename.

Revision ID: f1a2b3c4d5e6
Revises: aacf7d04b094
Create Date: 2026-08-28 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, None] = 'aacf7d04b094'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

RENAMES = [
    ("gstNumber", "gst_number"),
    ("panNumber", "pan_number"),
    ("documentMediaLink", "document_media_link"),
    ("documentVerificationDone", "document_verification_done"),
    ("documentVerificationDoneBy", "document_verification_done_by"),
    ("documentVerificationDoneAt", "document_verification_done_at"),
    ("businessName", "business_name"),
    ("legalName", "legal_name"),
    ("logoMediaId", "logo_media_id"),
    ("whatsappMobile", "whatsapp_mobile"),
    ("ownerName", "owner_name"),
    ("businessAddressLine1", "business_address_line1"),
    ("businessAddressLine2", "business_address_line2"),
    ("locationLatitude", "location_latitude"),
    ("locationLongitude", "location_longitude"),
    ("postOffice", "post_office"),
    ("policeStation", "police_station"),
    ("postalCode", "postal_code"),
    ("businessType", "business_type"),
    ("businessDescription", "business_description"),
    ("employeeCount", "employee_count"),
    ("registeredAt", "registered_at"),
]


def upgrade() -> None:
    for old_name, new_name in RENAMES:
        op.alter_column("tenants_details", old_name, new_column_name=new_name)


def downgrade() -> None:
    for old_name, new_name in RENAMES:
        op.alter_column("tenants_details", new_name, new_column_name=old_name)
