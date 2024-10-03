# FastAPI User Management API

This project is a FastAPI-based API for managing users. It connects to a PostgreSQL database using `SQLModel` and provides endpoints for adding and retrieving users.

## Features

- **User Management**: Add users to the PostgreSQL database.
- **FastAPI Framework**: Simple and lightweight Python framework.
- **SQLModel**: ORM for managing the database interactions.
- **PostgreSQL**: Backend database support with connection via `psycopg`.

## Requirements

- Python 3.8+
- PostgreSQL
- FastAPI
- SQLModel
- psycopg2
- uvicorn

## Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>


**pip install fastapi sqlmodel psycopg2-binary uvicorn**

`pip install fastapi sqlmodel psycopg2-binary uvicorn`


**Set up the database: Ensure PostgreSQL is installed and running. Update the DATABASE_URL in the app/settings.py file with your PostgreSQL credentials:**

`DATABASE_URL = "postgresql://username:password@localhost/dbname"`

**Run the application: Start the FastAPI server using Uvicorn:**

`poetry run uvicorn app.main:app --reload`

**The application will be running at http://127.0.0.1:8000.**


**Adds a new user to the database. Expects the following JSON body:**

{
 `"user_name": "John Doe",`
  `"user_address": "123 Main St",`
  `"user_email": "john.doe@example.com",`
  `"user_password": "password123"`
}

# Database

The project uses SQLModel for managing the connection and models for the PostgreSQL database.

# User Table

`user_id:` Primary key (Auto-incremented)
`user_name:` User's name
`user_address:` User's address
`user_email:` User's email
`user_password:` User's password (should be hashed in production)