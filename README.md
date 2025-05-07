# LeetCode Anki Revision App

## Description

This is a full-stack web application designed to help users revise LeetCode problems using the spaced repetition technique, similar to Anki flashcards. It allows users to add coding problems, track their solutions, and schedule reviews at increasing intervals (2, 4, 8, 16, 30 days).

## Features

*   View questions scheduled for revision today on the homepage.
*   Add new LeetCode questions with their solutions.
*   View individual question details and solutions.
*   Update question solutions.
*   Schedule the next revision date based on spaced repetition intervals (2, 4, 8, 16, 30 days).
*   Delete questions from the bank.
*   Containerized deployment using Docker.

## Technologies Used

*   **Frontend:** React, React Router, Axios
*   **Backend:** FastAPI (Python), Motor (Async MongoDB Driver), Pydantic
*   **Database:** MongoDB
*   **Containerization:** Docker, Docker Compose
*   **Backend Testing:** Pytest, HTTPX, Pytest-Asyncio

## Prerequisites

*   Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
*   Docker Compose: (Usually included with Docker Desktop) [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Setup & Running

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Environment Variables:**
    The application uses a `.env.backend.dev` file to configure the MongoDB connection for the backend service when running via Docker Compose. The `MONGO_USER` and `MONGO_PASS` variables from this file are used by `docker-compose.yml` to set up the MongoDB container and construct the `MONGO_DETAILS` connection string for the backend service. Ensure the database name in `MONGO_DETAILS` (`spaced_repetition`) matches the one used in the backend code (`backend/app/database.py`) and `MONGO_INITDB_DATABASE` in `docker-compose.yml`.

    *Default `.env.backend.dev`:*
    ```env
    MONGO_USER=mongo_user
    MONGO_PASS=mongo_pass
    ```

    *Connection string constructed in `docker-compose.yml`:*
    `MONGO_DETAILS=mongodb://${MONGO_USER}:${MONGO_PASS}@mongo:27017/spaced_repetition?authSource=admin`

3.  **Build and Run with Docker Compose:**
    This command will build the Docker images for the frontend and backend (if they don't exist) and start the frontend, backend, and MongoDB containers in detached mode.

    ```bash
    docker-compose up --build -d
    ```

4.  **Access the Application:**
    *   **Frontend:** Open your browser and navigate to `http://localhost:3000`
    *   **Backend API Docs:** Open your browser and navigate to `http://localhost:8000/docs`

5.  **Stopping the Application:**
    ```bash
    docker-compose down
    ```

## Running Backend Tests

To run the backend unit and integration tests, use the following Docker Compose command:

```bash
docker-compose run --rm backend pytest tests/
```
This command starts a temporary container for the backend service, installs development dependencies (using `requirements-dev.txt`), and executes the tests located in the `backend/tests` directory. The `--rm` flag ensures the container is removed after the tests finish. Make sure your `requirements-dev.txt` is present in the `backend` directory.

## Project Structure (Simplified)

```
.
├── backend/              # FastAPI backend source code, tests, Dockerfile, requirements*.txt
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
├── frontend/             # React frontend source code, Dockerfile, nginx.conf
│   ├── public/
│   ├── src/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── .env.backend.dev      # Backend environment variables for Docker Compose
├── .dockerignore         # Root dockerignore (if needed)
├── docker-compose.yml    # Docker Compose configuration
└── README.md             # This file
```
