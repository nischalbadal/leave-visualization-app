from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    userId = Column(String)
    empId = Column(String)
    teamManagerId = Column(String)
    firstName = Column(String)
    middleName = Column(String)
    lastName = Column(String)
    email = Column(String)
    isHr = Column(Boolean)
    isSupervisor = Column(Boolean)
    designationId = Column(String, ForeignKey('designations.id'))

class LeaveRequest(Base):
    __tablename__ = 'leave_requests'
    id = Column(String, primary_key=True)
    userId = Column(String, ForeignKey('users.id'))
    leaveIssuerId = Column(String)
    currentLeaveIssuerId = Column(String)
    leaveIssuerFirstName = Column(String)
    leaveIssuerLastName = Column(String)
    currentLeaveIssuerEmail = Column(String)
    departmentDescription = Column(String)
    startDate = Column(Date)
    endDate = Column(Date)
    leaveDays = Column(Integer)
    reason = Column(String)
    status = Column(String)
    remarks = Column(String)
    leaveTypeId = Column(String, ForeignKey('leave_types.id'))
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
    isConverted = Column(Boolean)
    fiscalId = Column(String, ForeignKey('fiscal_years.id'))

class LeaveType(Base):
    __tablename__ = 'leave_types'
    id = Column(String, primary_key=True)
    leaveTypeName = Column(String)
    defaultDays = Column(Integer)
    transferableDays = Column(Integer)
    isConsecutive = Column(Boolean)

class FiscalYear(Base):
    __tablename__ = 'fiscal_years'
    id = Column(String, primary_key=True)
    fiscalStartDate = Column(DateTime)
    fiscalEndDate = Column(DateTime)
    fiscalIsCurrent = Column(Boolean)

class Designation(Base):
    __tablename__ = 'designations'
    id = Column(String, primary_key=True)
    designationName = Column(String)

class Allocation(Base):
    __tablename__ = 'allocations'
    id = Column(String, primary_key=True)
    userId = Column(String, ForeignKey('users.id'))
    name = Column(String)
    type = Column(String)
