from typing import Sequence, Union

from alembic import op

revision: str = "e8f9a123b456"
down_revision: Union[str, None] = "df84845c699e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLES_WITH_RLS = [
    ("customers", "tenant_id"),
    ("stores", "tenant_id"),
    ("media_files", "tenant_id"),
    ("approvalRequests", "tenant_id"),
]


def upgrade() -> None:
    conn = op.get_bind()

    if conn.dialect.name != "postgresql":
        return

    for table_name, tenant_col in TABLES_WITH_RLS:
        op.execute(
            f'ALTER TABLE "{table_name}" ENABLE ROW LEVEL SECURITY;'
        )
        op.execute(
            f'ALTER TABLE "{table_name}" FORCE ROW LEVEL SECURITY;'
        )
        op.execute(
            f'''
            CREATE POLICY {table_name}_tenant_isolation_policy
            ON "{table_name}"
            USING ("{tenant_col}"::text = current_setting(
                'app.current_tenant_id', true
            ));
            '''
        )


def downgrade() -> None:
    conn = op.get_bind()

    if conn.dialect.name != "postgresql":
        return

    for table_name, _ in TABLES_WITH_RLS:
        op.execute(
            f'DROP POLICY IF EXISTS {table_name}_tenant_isolation_policy '
            f'ON "{table_name}";'
        )
        op.execute(
            f'ALTER TABLE "{table_name}" DISABLE ROW LEVEL SECURITY;'
        )
