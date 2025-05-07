import pytest
import pytest_asyncio # Required for async fixtures
import asyncio
from httpx import AsyncClient
from fastapi import FastAPI

# Import the app and database functions from your backend application
# Adjust the import path based on your project structure
from app.main import app as fastapi_app
from app.database import get_database, connect_to_mongo, close_mongo_connection

# Fixture for the event loop (required by pytest-asyncio)
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Fixture to manage MongoDB connection and cleanup
@pytest_asyncio.fixture(scope="function", autouse=True)
async def manage_db():
    """
    Connects to the database before tests, clears the 'questions' collection,
    and closes the connection after tests. Applied automatically to all test functions.
    """
    # Ensure connection is established (lifespan manager should handle this, but safety first)
    # Note: This assumes connect_to_mongo/close_mongo_connection are idempotent or handled correctly
    try:
        await connect_to_mongo()
        db = get_database()
        questions_collection = db["questions"]
        # Clear the collection before the test runs
        print(f"Clearing 'questions' collection before test...")
        await questions_collection.delete_many({})
        print("'questions' collection cleared.")
        yield # Test runs here
    finally:
        # Close connection after tests
        await close_mongo_connection()
        print("MongoDB connection closed after test.")


# Fixture to provide an HTTX async test client
@pytest_asyncio.fixture(scope="function")
async def test_client():
    """
    Provides an asynchronous test client for the FastAPI application,
    handling the application lifespan (startup/shutdown events).
    """
    # Use httpx.AsyncClient for testing async FastAPI apps
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        # Manually handle lifespan if needed, especially if manage_db isn't sufficient
        # However, AsyncClient with app=... often handles lifespan automatically.
        # If explicit control is needed:
        # async with client.lifespan(fastapi_app):
        #     yield client
        # For now, assume AsyncClient handles it or manage_db is sufficient
        print("Test client created.")
        yield client
        print("Test client teardown.")

# Note: The original plan mentioned a 'mock_db_connection' fixture.
# This implementation uses a real (test) database connection and clears the
# relevant collection before each test via the 'manage_db' fixture.
# This is often simpler for integration tests than extensive mocking.
# Ensure your MONGO_DETAILS points to a TEST database, not production!
