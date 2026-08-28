"""merge migration heads

Revision ID: d1cb39bfa6fb
Revises: 37d916d07c54, e8f9a123b456
Create Date: 2026-08-10 11:48:45.732300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1cb39bfa6fb'
down_revision: Union[str, None] = ('37d916d07c54', 'e8f9a123b456')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
