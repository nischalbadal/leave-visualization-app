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
    # Create the main raw_leave_data table with versioning columns
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
        sa.Column(
            "valid_from",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column("valid_to", sa.DateTime, nullable=False, server_default="infinity"),
    )

    # Create the history table
    op.create_table(
        "raw_leave_data_history",
        sa.Column("id", sa.Integer, nullable=False),
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
        sa.Column("valid_from", sa.DateTime, nullable=False),
        sa.Column("valid_to", sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint("id", "valid_from"),
    )

    # Create a trigger function for versioning
    op.execute(
        """
    CREATE OR REPLACE FUNCTION raw_leave_data_versioning()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Insert the old record into the history table
        INSERT INTO raw_leave_data_history (id, userId, empId, teamManagerId, designationId, designationName,
            firstName, middleName, lastName, email, isHr, isSupervisor, allocations,
            leaveIssuerId, currentLeaveIssuerId, leaveIssuerFirstName, leaveIssuerLastName,
            currentLeaveIssuerEmail, departmentDescription, startDate, endDate, leaveDays,
            reason, status, remarks, leaveTypeId, leaveTypeName, defaultDays, transferableDays,
            isConsecutive, fiscalId, fiscalStartDate, fiscalEndDate, fiscalIsCurrent,
            createdAt, updatedAt, isConverted, dataSource, valid_from, valid_to)
        VALUES (OLD.id, OLD.userId, OLD.empId, OLD.teamManagerId, OLD.designationId, OLD.designationName,
            OLD.firstName, OLD.middleName, OLD.lastName, OLD.email, OLD.isHr, OLD.isSupervisor,
            OLD.allocations, OLD.leaveIssuerId, OLD.currentLeaveIssuerId, OLD.leaveIssuerFirstName,
            OLD.leaveIssuerLastName, OLD.currentLeaveIssuerEmail, OLD.departmentDescription,
            OLD.startDate, OLD.endDate, OLD.leaveDays, OLD.reason, OLD.status, OLD.remarks,
            OLD.leaveTypeId, OLD.leaveTypeName, OLD.defaultDays, OLD.transferableDays,
            OLD.isConsecutive, OLD.fiscalId, OLD.fiscalStartDate, OLD.fiscalEndDate,
            OLD.fiscalIsCurrent, OLD.createdAt, OLD.updatedAt, OLD.isConverted, OLD.dataSource,
            OLD.valid_from, now());

        -- Update the current record's valid_to to now()
        NEW.valid_from := now();
        NEW.valid_to := 'infinity';

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
    )

    # Create the trigger for the main table
    op.execute(
        """
    CREATE TRIGGER update_raw_leave_data_versioning
    BEFORE UPDATE ON raw_leave_data
    FOR EACH ROW
    EXECUTE FUNCTION raw_leave_data_versioning();
    """
    )


def downgrade():
    # Drop the trigger
    op.execute(
        "DROP TRIGGER IF EXISTS update_raw_leave_data_versioning ON raw_leave_data;"
    )

    # Drop the versioning function
    op.execute("DROP FUNCTION IF EXISTS raw_leave_data_versioning();")

    # Drop the history table
    op.drop_table("raw_leave_data_history")

    # Drop the main table
    op.drop_table("raw_leave_data")
