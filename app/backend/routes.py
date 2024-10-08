from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from .models import UserAccount, User
from . import db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.DEBUG)

api = Blueprint("api", __name__)


@api.route("/health", methods=["GET"])
def health_check():
    return jsonify(status="healthy"), 200


@api.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = UserAccount.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad email or password"}), 401


@api.route("/register", methods=["POST"])
def register():
    data = request.json
    if UserAccount.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "Email already exists."}), 409

    new_user = UserAccount(
        email=data["email"], password=generate_password_hash(data["password"])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully!"}), 201


@api.route("/dashboard")
@jwt_required()
def dashboard():
    connection = db.engine.connect()

    try:
        dim_designations = (
            connection.execute(text("SELECT * FROM dim_designations")).mappings().all()
        )
        dim_fiscal_periods = (
            connection.execute(text("SELECT * FROM dim_fiscal_periods"))
            .mappings()
            .all()
        )
        dim_leave_types = (
            connection.execute(text("SELECT * FROM dim_leave_types")).mappings().all()
        )
        dim_users = connection.execute(text("SELECT * FROM dim_users")).mappings().all()
        dim_leave_issuer = (
            connection.execute(text("SELECT * FROM dim_leave_issuer")).mappings().all()
        )
        fact_leave_requests = (
            connection.execute(
                text(
                    'SELECT * FROM fact_leave_requests as flr inner join dim_leave_types as dlt on dlt."leaveTypeId"  = flr."leaveTypeId"'
                )
            )
            .mappings()
            .all()
        )
    finally:
        connection.close()

    return jsonify(
        {
            "dim_designations": [dict(row) for row in dim_designations],
            "dim_fiscal_periods": [dict(row) for row in dim_fiscal_periods],
            "dim_leave_types": [dict(row) for row in dim_leave_types],
            "dim_users": [dict(row) for row in dim_users],
            "dim_leave_issuer": [dict(row) for row in dim_leave_issuer],
            "fact_leave_requests": [dict(row) for row in fact_leave_requests],
        }
    )


@api.route("/employee/names", methods=["GET"])
@jwt_required()
def get_employee_names():
    employees = User.query.all()
    employee_names = [
        {"userId": emp.userId, "fullName": emp.fullName} for emp in employees
    ]
    return jsonify(employee_names), 200


@api.route("/employee/<string:user_id>", methods=["GET"])
@jwt_required()
def get_employee_details(user_id):
    employee = User.query.filter_by(userId=user_id).first()
    if not employee:
        return jsonify({"msg": "Employee not found."}), 404

    leave_records = employee.leave_requests
    leave_data = [
        {
            "leaveTypeId": lr.leaveTypeId,
            "leaveTypeName": lr.leave_type.leaveTypeName,
            "status": lr.status,
            "startDate": lr.startDate,
            "endDate": lr.endDate,
            "leaveDays": lr.leaveDays,
        }
        for lr in leave_records
    ]

    return (
        jsonify(
            {
                "employee_details": {
                    "userId": employee.userId,
                    "firstName": employee.firstName,
                    "middleName": employee.middleName,
                    "lastName": employee.lastName,
                    "email": employee.email,
                    "designationName": employee.designation.designationName
                    if employee.designation
                    else None,
                },
                "employee_leaves": leave_data,
            }
        ),
        200,
    )


@api.route('/tables', methods=['GET'])
@jwt_required()
def get_tables():
    return jsonify({
        "tables": [
            "dim_users",
            "dim_designations",
            "dim_fiscal_periods",
            "dim_leave_types",
            "dim_leave_issuer"
        ]
    })


@api.route('/table/<table_name>', methods=['GET'])
@jwt_required()
def get_table_data(table_name):
    try:
        with db.engine.connect() as conn:
            query = 'select flr.id, flr."departmentDescription", flr."startDate", flr."endDate", flr."leaveDays", flr.reason, flr.status, flr."isConverted", '

            join_conditions = {
                'dim_users': {
                    'join': 'JOIN dim_users du ON flr."userId" = du."userId"',
                    'columns': 'du."userId", du."empId", du."teamManagerId", du."firstName", du."middleName", du."lastName", du.email, du."isHr", du."isSupervisor"'
                },
                'dim_designations': {
                    'join': 'JOIN dim_users du ON flr."userId" = du."userId" '
                            'JOIN dim_designations dd ON du."designationId" = dd."designationId"',
                    'columns': 'du."userId", du."empId", du."teamManagerId", du."firstName", du."middleName", du."lastName", du.email, du."isHr", du."isSupervisor",dd."designationName" '
                },
                'dim_fiscal_periods': {
                    'join': 'JOIN dim_fiscal_periods dfp ON flr."fiscalId" = dfp."fiscalId"',
                    'columns': 'dfp."fiscalStartDate", dfp."fiscalEndDate", dfp."fiscalIsCurrent" '
                },
                'dim_leave_types': {
                    'join': 'JOIN dim_leave_types dlt ON flr."leaveTypeId" = dlt."leaveTypeId"',
                    'columns': 'dlt."leaveTypeName", dlt."defaultDays", dlt."transferableDays", dlt."isConsecutive"'
                },
                'dim_leave_issuer': {
                    'join': 'JOIN dim_leave_issuer dli ON flr."leaveIssuerId" = dli."leaveIssuerId"',
                    'columns': 'dli."leaveIssuerFirstName" , dli."leaveIssuerLastName", dli."leaveIssuerEmail" '
                }
            }

            if table_name in join_conditions:
                query += join_conditions[table_name]['columns'] + ' '
                query += 'FROM fact_leave_requests flr ' + join_conditions[table_name]['join']
            else:
                return jsonify({"error": "Invalid table name"}), 400

            query_result = conn.execute(text(query)).fetchall()

        result = [dict(row._mapping) for row in query_result]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
