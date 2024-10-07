"""create qc_reports table

Revision ID: ac84fec986a5
Revises: 9c3de66d8283
Create Date: 2024-10-07 21:55:23.003049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac84fec986a5'
down_revision: Union[str, None] = '9c3de66d8283'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'qc_reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('qc_name', sa.String(), nullable=False),
        sa.Column('qc_json', sa.JSON(), nullable=False),
        sa.Column('created_timestamp', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

def downgrade():
    op.drop_table('qc_reports')
