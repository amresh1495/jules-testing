import pytest
import json
from app import app  # Import the Flask app instance from app/__init__.py

@pytest.fixture
def client():
    """Create a Flask test client fixture."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset the in-memory database before each test
        # This requires access to the underlying db structure.
        # Let's import it directly for simplicity in testing.
        from app.models import employees_db, next_id as models_next_id

        # Reset the database to a known state
        global next_id # Use a local next_id for tests to avoid state leak
        next_id = 1
        def get_next_id_test():
            global next_id
            current_id = next_id
            next_id += 1
            return current_id

        # Monkeypatch the get_next_id in models for predictable IDs during tests
        # This is complex. A simpler approach for now might be to just clear and repopulate.
        # Let's stick to clearing and repopulating for simplicity here.

        employees_db.clear()
        initial_data = {
            1: {"name": "Alice", "position": "Software Engineer", "department": "Technology"},
            2: {"name": "Bob", "position": "Data Scientist", "department": "Analytics"},
        }
        employees_db.update(initial_data)
        # Reset the global next_id in models module based on initial data
        models_next_id = max(initial_data.keys() or [0]) + 1

        yield client
        # Clean up after test (optional, as fixture setup runs per test)
        employees_db.clear()
        models_next_id = 1


# --- Test Functions ---

def test_create_employee_success(client):
    """Test successful employee creation (POST /employees)."""
    new_employee_data = {"name": "Charlie", "position": "Product Manager", "department": "Product"}
    response = client.post('/employees', json=new_employee_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == new_employee_data['name']
    assert data['position'] == new_employee_data['position']
    assert data['department'] == new_employee_data['department']
    assert 'id' in data
    # Check if it was actually added to the db (using get)
    get_response = client.get(f'/employees/{data["id"]}')
    assert get_response.status_code == 200

def test_create_employee_bad_request(client):
    """Test employee creation with missing data (POST /employees)."""
    incomplete_data = {"name": "David"} # Missing position and department
    response = client.post('/employees', json=incomplete_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "Missing data" in data["error"]

def test_get_employees(client):
    """Test retrieving all employees (GET /employees)."""
    response = client.get('/employees')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2 # Based on the fixture setup
    assert data[0]['name'] == "Alice"
    assert data[1]['name'] == "Bob"
    assert 'id' in data[0]
    assert 'id' in data[1]

def test_get_employee_success(client):
    """Test retrieving a specific employee successfully (GET /employees/<id>)."""
    employee_id = 1 # Alice
    response = client.get(f'/employees/{employee_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == employee_id
    assert data['name'] == "Alice"
    assert data['position'] == "Software Engineer"

def test_get_employee_not_found(client):
    """Test retrieving a non-existent employee (GET /employees/<id>)."""
    non_existent_id = 999
    response = client.get(f'/employees/{non_existent_id}')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "not found" in data["error"]

def test_update_employee_success(client):
    """Test updating an existing employee successfully (PUT /employees/<id>)."""
    employee_id = 1 # Alice
    update_data = {"position": "Senior Software Engineer", "department": "Core Engineering"}
    response = client.put(f'/employees/{employee_id}', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == employee_id
    assert data['name'] == "Alice" # Name should not change
    assert data['position'] == update_data['position']
    assert data['department'] == update_data['department']
    # Verify change with a GET request
    get_response = client.get(f'/employees/{employee_id}')
    get_data = json.loads(get_response.data)
    assert get_data['position'] == update_data['position']

def test_update_employee_not_found(client):
    """Test updating a non-existent employee (PUT /employees/<id>)."""
    non_existent_id = 999
    update_data = {"name": "Ghost"}
    response = client.put(f'/employees/{non_existent_id}', json=update_data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "not found" in data["error"]

def test_delete_employee_success(client):
    """Test deleting an employee successfully (DELETE /employees/<id>)."""
    employee_id_to_delete = 2 # Bob
    response = client.delete(f'/employees/{employee_id_to_delete}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert "deleted successfully" in data["message"]
    # Verify deletion with a GET request
    get_response = client.get(f'/employees/{employee_id_to_delete}')
    assert get_response.status_code == 404

def test_delete_employee_not_found(client):
    """Test deleting a non-existent employee (DELETE /employees/<id>)."""
    non_existent_id = 999
    response = client.delete(f'/employees/{non_existent_id}')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
    assert "not found" in data["error"]
