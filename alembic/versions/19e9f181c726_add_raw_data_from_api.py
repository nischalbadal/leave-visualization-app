"""add raw data from API

Revision ID: 19e9f181c726
Revises: d57c4911a2c2
Create Date: 2024-06-12 10:59:39.315376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "19e9f181c726"
down_revision: Union[str, None] = "d57c4911a2c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the raw_leave_data table
    op.create_table(
        "raw_leave_data",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("userId", sa.Integer, nullable=False),
        sa.Column("empId", sa.String, nullable=False),
        sa.Column("teamManagerId", sa.Integer, nullable=True),
        sa.Column("designationId", sa.Integer, nullable=True),
        sa.Column("designationName", sa.String, nullable=True),
        sa.Column("firstName", sa.String, nullable=False),
        sa.Column("middleName", sa.String, nullable=True),
        sa.Column("lastName", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("isHr", sa.Boolean, nullable=True),
        sa.Column("isSupervisor", sa.Boolean, nullable=True),
        sa.Column("allocations", sa.JSON, nullable=True),
        sa.Column("leaveIssuerId", sa.Integer, nullable=True),
        sa.Column("currentLeaveIssuerId", sa.Integer, nullable=True),
        sa.Column("leaveIssuerFirstName", sa.String, nullable=True),
        sa.Column("leaveIssuerLastName", sa.String, nullable=True),
        sa.Column("currentLeaveIssuerEmail", sa.String, nullable=True),
        sa.Column("departmentDescription", sa.String, nullable=True),
        sa.Column("startDate", sa.DateTime, nullable=True),
        sa.Column("endDate", sa.DateTime, nullable=True),
        sa.Column("leaveDays", sa.Integer, nullable=True),
        sa.Column("reason", sa.String, nullable=True),
        sa.Column("status", sa.String, nullable=True),
        sa.Column("remarks", sa.String, nullable=True),
        sa.Column("leaveTypeId", sa.Integer, nullable=True),
        sa.Column("leaveTypeName", sa.String, nullable=True),
        sa.Column("defaultDays", sa.Integer, nullable=True),
        sa.Column("transferableDays", sa.Integer, nullable=True),
        sa.Column("isConsecutive", sa.Boolean, nullable=True),
        sa.Column("fiscalId", sa.Integer, nullable=True),
        sa.Column("fiscalStartDate", sa.DateTime, nullable=True),
        sa.Column("fiscalEndDate", sa.DateTime, nullable=True),
        sa.Column("fiscalIsCurrent", sa.Boolean, nullable=True),
        sa.Column("createdAt", sa.DateTime, nullable=True),
        sa.Column("updatedAt", sa.DateTime, nullable=True),
        sa.Column("isConverted", sa.Boolean, nullable=True),
        sa.Column("dataSource", sa.String, nullable=True),
        sa.Column(
            "ingestedDateTime",
            sa.DateTime,
            nullable=True,
            server_default=sa.func.current_timestamp(),
        ),
    )


def downgrade() -> None:
    # Drop the raw_leave_data table
    op.drop_table("raw_leave_data")
