from flask import Flask, request, jsonify
from app.models import employees_db, get_next_id

# Note: We will create the Flask app instance in app/__init__.py
# For now, we assume 'app' is the Flask instance to register routes.
# We will use a Blueprint later if needed, but for simplicity now,
# let's assume direct registration which requires the app object.
# We'll address this properly when setting up app/__init__.py.
# For now, let's just define the functions that will become routes.

def register_routes(app):

    @app.route('/employees', methods=['POST'])
    def create_employee():
        """Creates a new employee."""
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'position', 'department')):
            return jsonify({"error": "Missing data for required fields: name, position, department"}), 400

        new_id = get_next_id()
        new_employee = {
            "name": data['name'],
            "position": data['position'],
            "department": data['department']
        }
        employees_db[new_id] = new_employee
        return jsonify({**{"id": new_id}, **new_employee}), 201

    @app.route('/employees', methods=['GET'])
    def get_employees():
        """Retrieves all employees."""
        # Return a list of employees, including their IDs
        employee_list = [{**{"id": eid}, **edata} for eid, edata in employees_db.items()]
        return jsonify(employee_list), 200

    @app.route('/employees/<int:employee_id>', methods=['GET'])
    def get_employee(employee_id):
        """Retrieves a specific employee by ID."""
        employee = employees_db.get(employee_id)
        if employee:
            return jsonify({**{"id": employee_id}, **employee}), 200
        else:
            return jsonify({"error": "Employee not found"}), 404

    @app.route('/employees/<int:employee_id>', methods=['PUT'])
    def update_employee(employee_id):
        """Updates an existing employee."""
        if employee_id not in employees_db:
            return jsonify({"error": "Employee not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body cannot be empty"}), 400

        # Update only provided fields
        employee = employees_db[employee_id]
        if 'name' in data:
            employee['name'] = data['name']
        if 'position' in data:
            employee['position'] = data['position']
        if 'department' in data:
            employee['department'] = data['department']

        employees_db[employee_id] = employee
        return jsonify({**{"id": employee_id}, **employee}), 200

    @app.route('/employees/<int:employee_id>', methods=['DELETE'])
    def delete_employee(employee_id):
        """Deletes an employee."""
        if employee_id in employees_db:
            del employees_db[employee_id]
            return jsonify({"message": "Employee deleted successfully"}), 200
        else:
            return jsonify({"error": "Employee not found"}), 404
