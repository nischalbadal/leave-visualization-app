from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Designation(db.Model):
    __tablename__ = 'dim_designations'

    designationId = Column(String, primary_key=True)
    designationName = Column(String)

    # Back reference for users
    users = relationship("User", back_populates="designation")

    def __repr__(self):
        return f"<Designation(id={self.designationId}, name={self.designationName})>"


class FiscalYear(db.Model):
    __tablename__ = 'dim_fiscal_years'

    fiscalId = Column(String, primary_key=True)
    fiscalStartDate = Column(DateTime)
    fiscalEndDate = Column(DateTime)
    fiscalIsCurrent = Column(Boolean)

    # Back reference for leave requests
    leave_requests = relationship("LeaveRequest", back_populates="fiscal_year")

    def __repr__(self):
        return f"<FiscalYear(id={self.fiscalId}, start={self.fiscalStartDate}, end={self.fiscalEndDate})>"


class LeaveType(db.Model):
    __tablename__ = 'dim_leave_types'

    leaveTypeId = Column(String, primary_key=True)
    leaveTypeName = Column(String)
    defaultDays = Column(Integer)
    transferableDays = Column(Integer)
    isConsecutive = Column(Boolean)

    # Back reference for leave requests
    leave_requests = relationship("LeaveRequest", back_populates="leave_type")

    def __repr__(self):
        return f"<LeaveType(id={self.leaveTypeId}, name={self.leaveTypeName})>"


class User(db.Model):
    __tablename__ = 'dim_users'

    userId = Column(String, primary_key=True)
    empId = Column(String)
    teamManagerId = Column(String)
    firstName = Column(String)
    middleName = Column(String)
    lastName = Column(String)
    email = Column(String)
    isHr = Column(Boolean)
    isSupervisor = Column(Boolean)
    designationId = Column(String, ForeignKey('dim_designations.designationId'))

    designation = relationship("Designation", back_populates="users")

    # Relationship with Allocations
    allocations = relationship("Allocation", back_populates="user")

    # Relationship with Leave Requests
    leave_requests = relationship("LeaveRequest", back_populates="user")  # Added this line

    @property
    def fullName(self):
        return f"{self.firstName} {self.middleName or ''} {self.lastName}".strip()

    def __repr__(self):
        return f"<User(id={self.userId}, name={self.fullName})>"


class Allocation(db.Model):
    __tablename__ = 'allocations'

    allocationId = Column(String, primary_key=True)
    userId = Column(String, ForeignKey('dim_users.userId'))  # Ensure this points to dim_users
    name = Column(String)
    type = Column(String)

    user = relationship("User", back_populates="allocations")  # Ensure this line is correct

    def __repr__(self):
        return f"<Allocation(id={self.allocationId}, user={self.userId}, name={self.name})>"


class LeaveRequest(db.Model):
    __tablename__ = 'fact_leave_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(String, ForeignKey('dim_users.userId'))
    leaveIssuerId = Column(String, ForeignKey('dim_leave_issuer.leaveIssuerId'))
    currentLeaveIssuerId = Column(String, ForeignKey('dim_leave_issuer.leaveIssuerId'))
    departmentDescription = Column(String)
    startDate = Column(Date)
    endDate = Column(Date)
    leaveDays = Column(Integer)
    reason = Column(String)
    status = Column(String)
    remarks = Column(String)
    leaveTypeId = Column(String, ForeignKey('dim_leave_types.leaveTypeId'))
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    isConverted = Column(Boolean)
    fiscalId = Column(String, ForeignKey('dim_fiscal_years.fiscalId'))

    user = relationship("User", back_populates="leave_requests")  # This line establishes the relationship
    leave_type = relationship("LeaveType", back_populates="leave_requests")
    fiscal_year = relationship("FiscalYear", back_populates="leave_requests")

    def __repr__(self):
        return f"<LeaveRequest(id={self.id}, user={self.userId}, status={self.status})>"


class LeaveIssuer(db.Model):
    __tablename__ = 'dim_leave_issuer'

    leaveIssuerId = Column(String, primary_key=True)
    leaveIssuerFirstName = Column(String)
    leaveIssuerLastName = Column(String)
    leaveIssuerEmail = Column(String)

    @property
    def leaveIssuerFullName(self):
        return f"{self.leaveIssuerFirstName} {self.leaveIssuerLastName}".strip()

    def __repr__(self):
        return f"<LeaveIssuer(id={self.leaveIssuerId}, first_name={self.leaveIssuerFirstName}, last_name={self.leaveIssuerLastName})>"


class UserAccount(db.Model):
    __tablename__ = 'user_accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=500), unique=True, nullable=False)
    password = Column(String(length=500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserAccount(email={self.email})>"
