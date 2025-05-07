from fastapi import FastAPI, HTTPException, Body, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Annotated
from bson import ObjectId
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from datetime import datetime, timedelta # Import datetime and timedelta

from .models import Question, QuestionUpdate, PyObjectId
from .database import connect_to_mongo, close_mongo_connection, get_database

# Lifespan manager for MongoDB connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await connect_to_mongo()
    yield
    print("Shutting down...")
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

# CORS configuration
origins = [
    "http://localhost:3000", # Allow frontend origin
    # Add other origins if needed, e.g., production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)

# Dependency to get the database collection
async def get_questions_collection():
    db = get_database()
    return db["questions"]

# Type alias for the collection dependency
QuestionsCollectionDep = Annotated[get_database, Depends(get_questions_collection)]

# Helper function to convert Question document to Question model
# This handles the ObjectId conversion for '_id'
def question_helper(question_data) -> Question:
    # Manually convert ObjectId to string if present
    if "_id" in question_data:
        question_data["_id"] = str(question_data["_id"])
    return Question(**question_data)


@app.post(
    "/questions/",
    response_model=Question,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new question",
)
async def add_question(
    collection: QuestionsCollectionDep,
    question: Question = Body(...),
):
    """
    Add a new question to the database.
    The `id` field is ignored if provided, as MongoDB generates it.
    """
    # Ensure we don't insert a client-provided ID
    question_dict = question.model_dump(exclude={"id"}, by_alias=True) # Use alias _id
    # Pydantic v2 doesn't automatically exclude None, but mongo requires _id to be ObjectId or absent
    if "_id" in question_dict and question_dict["_id"] is None:
         del question_dict["_id"]

    result: InsertOneResult = await collection.insert_one(question_dict)
    if result.inserted_id:
        # Retrieve the newly created question to include the generated ID
        new_question = await collection.find_one({"_id": result.inserted_id})
        if new_question:
            return question_helper(new_question) # Convert to Question model
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Question could not be added.")


@app.get(
    "/questions/",
    response_model=List[Question],
    summary="Get all questions",
)
async def get_all_questions(collection: QuestionsCollectionDep):
    """
    Retrieve all questions that are due for revision (next_revision_date <= now).
    """
    now = datetime.utcnow()
    questions = []
    # Filter for questions due for revision
    async for q in collection.find({"next_revision_date": {"$lte": now}}):
        questions.append(question_helper(q))
    return questions


@app.get(
    "/questions/{question_id}",
    response_model=Question,
    summary="Get a specific question by ID",
)
async def get_question(
    question_id: PyObjectId, # Use the custom type for validation
    collection: QuestionsCollectionDep,
):
    """
    Retrieve a single question by its unique ID.
    """
    try:
        obj_id = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format")

    question = await collection.find_one({"_id": obj_id})
    if question:
        return question_helper(question)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with id {question_id} not found")


@app.put(
    "/questions/{question_id}",
    response_model=Question,
    summary="Update a question",
)
async def update_question(
    question_id: PyObjectId,
    collection: QuestionsCollectionDep,
    question_update: QuestionUpdate = Body(...),
):
    """
    Update fields of an existing question.
    Only provided fields will be updated.
    """
    try:
        obj_id = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format")

    # Get update data, excluding unset fields to avoid overwriting with None
    update_data = question_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided")

    # --- Spaced Repetition Logic ---
    # Check if current_interval_days is provided for update
    if question_update.current_interval_days is not None:
        # Calculate the next revision date based on the provided interval
        now = datetime.utcnow()
        new_next_revision_date = now + timedelta(days=question_update.current_interval_days)
        update_data["next_revision_date"] = new_next_revision_date
        # Ensure current_interval_days itself is included in the update
        update_data["current_interval_days"] = question_update.current_interval_days

    result: UpdateResult = await collection.update_one(
        {"_id": obj_id}, {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with id {question_id} not found")

    # Retrieve and return the updated question
    updated_question = await collection.find_one({"_id": obj_id})
    if updated_question:
        return question_helper(updated_question)

    # This should ideally not happen if update was successful, but as a fallback
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found after update attempt.")


@app.delete(
    "/questions/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a question",
)
async def delete_question(
    question_id: PyObjectId,
    collection: QuestionsCollectionDep,
):
    """
    Delete a question from the database by its ID.
    """
    try:
        obj_id = ObjectId(question_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format")

    result: DeleteResult = await collection.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with id {question_id} not found")

    # No content to return on successful deletion
    return None
