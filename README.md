# Employee Management API

## Description

A simple Flask-based REST API for managing employee records. It allows creating, reading, updating, and deleting employee information stored in memory.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the Flask development server:

```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`.

## Running Tests

To run the unit tests using pytest:

```bash
pytest
```

## API Endpoints

The base URL is `http://127.0.0.1:5000`.

### Create Employee

*   **Method:** `POST`
*   **Path:** `/employees`
*   **Description:** Adds a new employee record.
*   **Request Body (JSON):**
    ```json
    {
        "name": "John Doe",
        "position": "Software Developer",
        "department": "Engineering"
    }
    ```
*   **Response (Success - 201 Created):**
    ```json
    {
        "id": 3, # ID will vary based on current state
        "name": "John Doe",
        "position": "Software Developer",
        "department": "Engineering"
    }
    ```
*   **Response (Error - 400 Bad Request):** If required fields are missing.
    ```json
    {
        "error": "Missing data for required fields: name, position, department"
    }
    ```

### Get All Employees

*   **Method:** `GET`
*   **Path:** `/employees`
*   **Description:** Retrieves a list of all employees.
*   **Response (Success - 200 OK):**
    ```json
    [
        {
            "id": 1,
            "name": "Alice",
            "position": "Software Engineer",
            "department": "Technology"
        },
        {
            "id": 2,
            "name": "Bob",
            "position": "Data Scientist",
            "department": "Analytics"
        }
        # Initial sample data
    ]
    ```

### Get Specific Employee

*   **Method:** `GET`
*   **Path:** `/employees/<employee_id>`
*   **Description:** Retrieves details for a specific employee by their ID.
*   **URL Parameters:**
    *   `employee_id` (integer): The unique ID of the employee.
*   **Response (Success - 200 OK):**
    ```json
    {
        "id": 1,
        "name": "Alice",
        "position": "Software Engineer",
        "department": "Technology"
    }
    ```
*   **Response (Error - 404 Not Found):** If the employee ID does not exist.
    ```json
    {
        "error": "Employee not found"
    }
    ```

### Update Employee

*   **Method:** `PUT`
*   **Path:** `/employees/<employee_id>`
*   **Description:** Updates details for an existing employee. Fields not provided in the request body will remain unchanged.
*   **URL Parameters:**
    *   `employee_id` (integer): The unique ID of the employee to update.
*   **Request Body (JSON):** (Include fields to update)
    ```json
    {
        "position": "Senior Software Engineer",
        "department": "Core Engineering"
    }
    ```
*   **Response (Success - 200 OK):**
    ```json
    {
        "id": 1,
        "name": "Alice", // Unchanged
        "position": "Senior Software Engineer", // Updated
        "department": "Core Engineering" // Updated
    }
    ```
*   **Response (Error - 404 Not Found):** If the employee ID does not exist.
    ```json
    {
        "error": "Employee not found"
    }
    ```
*   **Response (Error - 400 Bad Request):** If the request body is empty.
    ```json
    {
        "error": "Request body cannot be empty"
    }
    ```

### Delete Employee

*   **Method:** `DELETE`
*   **Path:** `/employees/<employee_id>`
*   **Description:** Deletes an employee record by their ID.
*   **URL Parameters:**
    *   `employee_id` (integer): The unique ID of the employee to delete.
*   **Response (Success - 200 OK):**
    ```json
    {
        "message": "Employee deleted successfully"
    }
    ```
*   **Response (Error - 404 Not Found):** If the employee ID does not exist.
    ```json
    {
        "error": "Employee not found"
    }
    ```

## Deployment

A `Dockerfile` is included in the project root for building a container image of the application. You can build and run the container using Docker.

```bash
# Build the image
docker build -t employee-api .

# Run the container
docker run -p 5000:5000 employee-api
```
The API will then be accessible at `http://localhost:5000`.
