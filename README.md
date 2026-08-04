# DATAforge

DATAforge is a backend-first data engineering project for uploading datasets, storing ingestion metadata, and generating an initial quality profile for each file. At its current stage, the project acts as the foundation for a self-service ETL platform: users can submit raw CSV, Excel, or JSON files, and the API validates the upload, saves the artifact, records it in the database, and returns a first-pass dataset analysis powered by Pandas.

The codebase already follows a clean layered structure with routers, services, repositories, models, and shared configuration. That makes it a solid base for expanding into cleaning pipelines, report generation, authentication, and broader workflow orchestration.

## Project Vision

The long-term goal of DATAforge is to become a lightweight self-service data operations platform where users can:

- upload raw business datasets,
- inspect structure and quality issues quickly,
- run cleaning or transformation pipelines,
- persist dataset metadata for traceability,
- generate reports from processed data,
- expose repeatable workflows through a clean API.

Right now, the implemented core is the ingestion and dataset analysis layer.

## What Is Implemented So Far

### Current capabilities

- FastAPI application setup with lifecycle bootstrapping.
- SQLAlchemy-based database connection and table creation.
- File upload endpoint at `POST /upload`.
- Validation for supported file types: `.csv`, `.xlsx`, `.json`.
- File size validation using environment-driven limits.
- Unique filename generation for safe storage.
- Local storage of uploaded datasets in the `uploads/` directory.
- Dataset metadata persistence in the `datasets` table.
- Pandas-based profiling that returns:
  - row count,
  - column count,
  - column names,
  - data types,
  - estimated memory usage,
  - descriptive statistics,
  - missing value counts,
  - duplicate row counts.

### Present but not wired yet

- `app/routers/datasets.py`
- `app/routers/reports.py`
- `app/routers/pipelines.py`
- `app/routers/auth.py`
- `cleaned/` directory for future processed outputs
- `reports/` directory for future generated reporting artifacts

## System Flow

### High-level request flow

```mermaid
flowchart TD
    A[Client uploads dataset] --> B[FastAPI /upload endpoint]
    B --> C[UploadService validates file type and size]
    C --> D[File stored in uploads directory]
    D --> E[DatasetService reads file with Pandas]
    E --> F[Generate summary statistics]
    F --> G[Check missing values and duplicates]
    G --> H[Create Dataset metadata record]
    H --> I[SQLAlchemy writes to database]
    I --> J[API returns upload result + analysis]
```

### Internal backend architecture

```mermaid
flowchart LR
    A[Client] --> B[FastAPI Router]
    B --> C[Service Layer]
    C --> D[Repository Layer]
    D --> E[(Database)]
    C --> F[Local File Storage]
    C --> G[Pandas Analysis Engine]
```

### Upload processing sequence

```mermaid
sequenceDiagram
    participant U as User / Client
    participant R as Upload Router
    participant S as UploadService
    participant D as DatasetService
    participant P as DatasetRepository
    participant DB as Database

    U->>R: POST /upload with file
    R->>S: Forward UploadFile + DB session
    S->>S: Validate extension
    S->>S: Validate file size
    S->>S: Save file with UUID filename
    S->>D: analyze_dataset(file_path, extension)
    D->>D: Read dataset with Pandas
    D->>D: Build summary, stats, null checks, duplicate checks
    D-->>S: Return dataset analysis
    S->>P: Create dataset metadata record
    P->>DB: Insert and commit
    DB-->>P: Persisted dataset
    P-->>S: Saved record
    S-->>R: Upload response payload
    R-->>U: JSON response
```

## Tech Stack

| Layer | Technology | Role in Project |
|---|---|---|
| API framework | FastAPI | Exposes HTTP endpoints and manages request handling |
| ASGI server | Uvicorn | Runs the application locally and in Docker |
| ORM / DB access | SQLAlchemy 2.x | Handles models, sessions, and persistence |
| Database driver | psycopg2-binary | PostgreSQL connectivity |
| Configuration | Pydantic Settings + dotenv | Environment-based configuration loading |
| Data processing | Pandas | Reads uploaded files and generates dataset analysis |
| Containerization | Docker | Packages the backend service for consistent runtime |
| Orchestration | Docker Compose | Starts the application container in development |
| Language | Python 3.11 | Core implementation language |

## Project Structure

```text
DATAforge/
├── app/
│   ├── core/             # App settings and configuration
│   ├── database/         # SQLAlchemy engine, base, session handling
│   ├── models/           # Database models
│   ├── repositories/     # Persistence logic
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic and dataset analysis
│   ├── utils/            # Shared utilities such as logging
│   └── main.py           # FastAPI entrypoint
├── uploads/              # Raw uploaded datasets
├── cleaned/              # Future cleaned dataset outputs
├── reports/              # Future generated report outputs
├── tests/                # Automated tests
├── Dockerfile            # Container definition
├── docker-compose.yml    # Local container setup
├── requirements.txt      # Python dependencies
└── README.md             # GitHub project overview
```

## Implemented Components

### 1. API layer

`app/main.py` initializes the FastAPI application, creates tables during startup, and exposes a basic health-style root endpoint. The upload router is the only route currently mounted.

### 2. Upload layer

`app/routers/upload.py` receives incoming files and injects a database session. It delegates the actual processing to the service layer instead of mixing validation and persistence in the route itself.

### 3. Service layer

`app/services/upload_service.py` is the main orchestration unit today. It:

- validates allowed file extensions,
- enforces the max upload size,
- writes the file to disk,
- calls dataset analysis,
- constructs the dataset metadata object,
- persists the record through the repository,
- returns a structured API response.

`app/services/dataset_service.py` handles dataset profiling. It reads supported file types into a Pandas DataFrame and computes summary information and quality indicators.

### 4. Persistence layer

`app/models/dataset.py` defines the `datasets` table used to store upload metadata.

`app/repositories/dataset_repository.py` currently contains the create operation for dataset records.

`app/database/database.py` sets up the SQLAlchemy engine, declarative base, session factory, and dependency-injected DB session lifecycle.

### 5. Configuration and utilities

`app/core/config.py` loads runtime configuration from `.env` and ensures required storage directories exist.

`app/utils/logger.py` provides application logging configuration.

## API Snapshot

### `GET /`

Returns a simple status payload:

```json
{
  "message": "Welcome to DataForge",
  "version": "1.0.0",
  "status": "running"
}
```

### `POST /upload`

Uploads a dataset file and returns persisted metadata plus a data profile.

Supported formats:

- CSV
- Excel (`.xlsx`)
- JSON

Example response shape:

```json
{
  "message": "File uploaded successfully",
  "dataset_id": "generated-uuid",
  "filename": "sales_data.csv",
  "status": "UPLOADED",
  "file_size_mb": 1.42,
  "analysis": {
    "summary": {},
    "statistics": {},
    "missing_values": {},
    "duplicate_rows": 0
  }
}
```

## Local Development

### Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure your database URL.
4. Start the API:

```bash
uvicorn app.main:app --reload
```

### Example environment configuration

```env
DATABASE_URL=postgresql://postgres:your_actual_password@localhost:5432/dataforge
UPLOAD_DIR=uploads
CLEANED_DIR=cleaned
REPORTS_DIR=reports
MAX_FILE_SIZE_MB=50
```

### Run with Docker

```bash
docker compose up --build
```

Note: the current `docker-compose.yml` starts the application container, but it does not yet provision a PostgreSQL service automatically. You still need a reachable database configured through `DATABASE_URL`.

## Current State and Next Logical Steps

The project already demonstrates a good backend foundation and clear separation of concerns. The next logical product milestones would be:

- mount and implement dataset listing and detail endpoints,
- add cleaning and transformation pipeline execution,
- generate downloadable reports into `reports/`,
- add authentication and user-scoped dataset ownership,
- introduce automated tests for upload and profiling flows,
- add stronger error handling for malformed files,
- expand Docker Compose to include PostgreSQL.

## Notes

- The repository structure suggests a broader ETL platform roadmap, but the active feature set is currently centered on ingestion and profiling.
- The code imports Pandas-based analysis logic, so the runtime environment should include data-processing dependencies required for CSV, Excel, and JSON parsing.

