employees_db = {}
next_id = 1

def get_next_id():
    """Generates the next unique ID for an employee."""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

# Initialize with some sample data
employees_db = {
    get_next_id(): {"name": "Alice", "position": "Software Engineer", "department": "Technology"},
    get_next_id(): {"name": "Bob", "position": "Data Scientist", "department": "Analytics"},
    get_next_id(): {"name": "Charlie", "position": "Product Manager", "department": "Product"},
}
