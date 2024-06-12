from flask import Flask, request, jsonify
from app.models import db, Employee, Leave

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.as_dict() for employee in employees])

@app.route('/api/leaves', methods=['GET'])
def get_leaves():
    leaves = Leave.query.all()
    return jsonify([leave.as_dict() for leave in leaves])

# Utility functions to convert ORM objects to dictionaries
def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

Employee.as_dict = to_dict
Leave.as_dict = to_dict

if __name__ == "__main__":
    app.run(debug=True)
