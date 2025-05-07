import pytest
from httpx import AsyncClient
from fastapi import status
from datetime import datetime, timedelta, timezone

# Mark all tests in this module as asyncio
pytestmark = pytest.mark.asyncio

# Helper function to create a question with a specific revision date
async def create_test_question(client: AsyncClient, text: str, solution: str, rev_date: datetime):
    question_data = {
        "question_text": text,
        "solution": solution,
        "next_revision_date": rev_date.isoformat(), # Pass as ISO string
        "current_interval_days": 0 # Default interval
    }
    response = await client.post("/questions/", json=question_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()

# --- Test Functions ---

async def test_get_all_questions_empty(test_client: AsyncClient):
    """Test getting questions when the database is empty (cleared by fixture)."""
    response = await test_client.get("/questions/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

async def test_create_question(test_client: AsyncClient):
    """Test creating a new question."""
    now = datetime.now(timezone.utc)
    question_data = {
        "question_text": "What is FastAPI?",
        "solution": "A modern, fast (high-performance) web framework for building APIs.",
        "next_revision_date": now.isoformat(), # Due now
        "current_interval_days": 1 # Example interval
    }
    response = await test_client.post("/questions/", json=question_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["question_text"] == question_data["question_text"]
    assert data["solution"] == question_data["solution"]
    # Compare dates by parsing back to datetime objects for robustness
    assert datetime.fromisoformat(data["next_revision_date"].replace("Z", "+00:00")) == now
    assert data["current_interval_days"] == question_data["current_interval_days"]
    assert "id" in data

async def test_get_all_questions_with_data(test_client: AsyncClient):
    """Test getting questions when one is due."""
    now = datetime.now(timezone.utc)
    created_question = await create_test_question(test_client, "Due Q", "Sol", now)

    response = await test_client.get("/questions/")
    assert response.status_code == status.HTTP_200_OK
    questions = response.json()
    assert len(questions) == 1
    assert questions[0]["id"] == created_question["id"]
    assert questions[0]["question_text"] == "Due Q"

async def test_get_specific_question(test_client: AsyncClient):
    """Test getting a specific question by its ID."""
    now = datetime.now(timezone.utc)
    created_question = await create_test_question(test_client, "Specific Q", "Detail", now)
    question_id = created_question["id"]

    response = await test_client.get(f"/questions/{question_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == question_id
    assert data["question_text"] == "Specific Q"
    assert data["solution"] == "Detail"

async def test_get_nonexistent_question(test_client: AsyncClient):
    """Test getting a question with an invalid/non-existent ID."""
    invalid_id = "605c7f7f7f7f7f7f7f7f7f7f" # Example valid ObjectId format, but likely non-existent
    response = await test_client.get(f"/questions/{invalid_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_update_question_schedule(test_client: AsyncClient):
    """Test updating the schedule (interval and next revision date) of a question."""
    now = datetime.now(timezone.utc)
    created_question = await create_test_question(test_client, "Update Q", "Initial", now)
    question_id = created_question["id"]
    update_interval = 10 # Days

    # Update the schedule
    update_response = await test_client.put(
        f"/questions/{question_id}",
        json={"current_interval_days": update_interval}
    )
    assert update_response.status_code == status.HTTP_200_OK
    updated_data = update_response.json()
    assert updated_data["current_interval_days"] == update_interval

    # Verify the update by getting the question again
    get_response = await test_client.get(f"/questions/{question_id}")
    assert get_response.status_code == status.HTTP_200_OK
    final_data = get_response.json()

    # Check if the interval is updated
    assert final_data["current_interval_days"] == update_interval

    # Check if next_revision_date is updated (approximately correct)
    expected_revision_date = datetime.now(timezone.utc) + timedelta(days=update_interval)
    actual_revision_date = datetime.fromisoformat(final_data["next_revision_date"].replace("Z", "+00:00"))

    # Allow a small tolerance (e.g., a few seconds) for processing time between PUT and check
    assert abs(actual_revision_date - expected_revision_date) < timedelta(seconds=10)

async def test_delete_question(test_client: AsyncClient):
    """Test deleting a question."""
    now = datetime.now(timezone.utc)
    created_question = await create_test_question(test_client, "Delete Q", "Gone", now)
    question_id = created_question["id"]

    # Delete the question
    delete_response = await test_client.delete(f"/questions/{question_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Verify deletion by trying to get it again
    get_response = await test_client.get(f"/questions/{question_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

async def test_spaced_repetition_filter(test_client: AsyncClient):
    """Test that GET /questions/ only returns questions due for revision."""
    now = datetime.now(timezone.utc)
    due_today_date = now - timedelta(days=1) # Ensure it's in the past
    due_tomorrow_date = now + timedelta(days=1)

    # Create one question due today (or earlier)
    due_question = await create_test_question(test_client, "Due Today", "Revise me", due_today_date)
    # Create one question due tomorrow
    not_due_question = await create_test_question(test_client, "Due Tomorrow", "Wait", due_tomorrow_date)

    # Get questions - should only return the one due today
    response = await test_client.get("/questions/")
    assert response.status_code == status.HTTP_200_OK
    questions = response.json()

    assert len(questions) == 1
    assert questions[0]["id"] == due_question["id"]
    assert questions[0]["question_text"] == "Due Today"

    # Verify the not-due question is not in the list
    question_ids_returned = [q["id"] for q in questions]
    assert not_due_question["id"] not in question_ids_returned
