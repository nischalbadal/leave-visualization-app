"""create pipeline_logs table

Revision ID: 6a1ed01895db
Revises: ac84fec986a5
Create Date: 2024-10-07 21:56:00.913270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6a1ed01895db"
down_revision: Union[str, None] = "ac84fec986a5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "pipeline_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_type", sa.String(), nullable=False),
        sa.Column("source_name", sa.String(), nullable=False, default="api_data"),
        sa.Column(
            "status",
            sa.Enum("COMPLETED", "FAILED", name="pipeline_status"),
            nullable=False,
        ),
        sa.Column(
            "created_timestamp",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade():
    op.execute("DROP TYPE pipeline_status")
    op.drop_table("pipeline_logs")
