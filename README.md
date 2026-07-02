# DATAforge

DATAforge is a starter FastAPI project scaffold for data processing workflows.

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a PostgreSQL database named `dataforge`.
4. Update `.env` with your real PostgreSQL password.
5. Run the app: `uvicorn app.main:app --reload`

Example:

`DATABASE_URL=postgresql://postgres:your_actual_password@localhost:5432/dataforge`

## Structure

- `app/` contains the FastAPI application package.
- `uploads/`, `cleaned/`, `reports/` are workspace folders for data artifacts.
- `tests/` contains automated tests.
