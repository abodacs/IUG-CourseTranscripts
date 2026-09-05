# IUG Course Transcripts

This project is a data pipeline for processing YouTube video transcripts for the Islamic University of Gaza (IUG).

## Project Explanation

The primary goal of this project is to fetch, process, and clean YouTube video transcripts for IUG courses. The pipeline consists of several Python scripts that work together to achieve this.

### Workflow

The pipeline is now organized into modules under the `src/` directory:

1.  **Data Extraction (`src/etl/extract.py`):**
    *   Fetches video and playlist data from YouTube using `yt-dlp`.
    *   Downloads raw transcript files (in JSON format) from an R2 bucket.
    *   Saves data into `.xlsx` files and organizes transcripts in the `data/` directory by playlist ID.

2.  **Data Loading (`src/etl/load.py`):**
    *   Reads video data from `.xlsx` files and inserts it into a Turso/SQLite database (`youtube-iug.db`).
    *   Updates sync status for downloaded transcripts.

3.  **Data Transformation (`src/etl/transform.py`):**
    *   Converts raw JSON transcripts into SRT (subtitle) format.
    *   Applies formatting rules and uses AI to correct typos in transcripts.

4.  **AI Processing (`src/ai/gemini.py`):**
    *   Handles AI-powered operations using Gemini API.
    *   Used for typo correction and content enhancement.

5.  **Database Management (`src/database.py`):**
    *   Manages database connections and synchronization operations.

6.  **Configuration (`src/config.py`):**
    *   Handles environment variables and configuration settings.

## Onboarding Plan

### 1. Environment Setup

To run these scripts, you will need to set up your environment:

*   **Install Dependencies:** This project uses `uv` for dependency management. Install the required Python packages:

    ```bash
    uv sync
    ```

*   **Create `.env` file:** The scripts use a `.env` file to manage secrets like API keys and database URLs. Create a `.env` file in the root of the project and add the necessary credentials. You can use the `.env.example` below as a template.

    ```
    TURSO_DATABASE_URL=""
    TURSO_AUTH_TOKEN=""
    bucket_name=""
    aws_access_key_id=""
    aws_secret_access_key=""
    endpoint_url=""
    GEMINI_API_KEY=""
    OPENAI_API_KEY=""
    ```

### 2. Examine the Data Flow

The data flows through the system in the following order:

1.  **Extract**: Creates Excel files from YouTube and downloads raw transcripts from R2.
2.  **Load**: Populates the database from Excel files and updates sync status.
3.  **Transform**: Processes raw JSON transcripts into SRT format and applies AI-powered corrections.

### 3. Understand the Configuration

*   **`.env` and `os.environ`:** The scripts use a `.env` file to manage secrets.
*   **Prompts:** The `prompt_clarify_transcript.txt` and `prompt_playlist.txt` files are used to instruct the AI models.

### 4. Explore the Database

*   The database schema is implicitly defined in the scripts. The main tables appear to be `playlists` and `sync_github`.
*   `src/database.py` contains database utility functions.

### 5. Running the Pipeline

The entire pipeline is now executed through a single main script:

```bash
uv run python main.py
```

This will run the complete ETL pipeline including:
1. Database synchronization
2. Data extraction from YouTube
3. Loading data into the database
4. Downloading raw transcripts from R2
5. Processing and transforming transcripts with AI corrections

### 6. Testing

**Current Status**: This project currently lacks automated tests, which makes refactoring and adding new features risky.

**Recommended Testing Strategy**:

*   **Unit Tests**: Test individual functions in isolation, especially:
    *   Database operations in `src/database.py`
    *   ETL functions in `src/etl/` modules
    *   AI processing functions in `src/ai/gemini.py`
    *   Utility functions in `src/utils.py`

*   **Integration Tests**: Test the entire pipeline flow:
    *   End-to-end pipeline execution
    *   Database connectivity and data integrity
    *   File I/O operations

*   **Setup Instructions**:
    ```bash
    # Add pytest to development dependencies
    uv add --dev pytest pytest-cov pytest-mock

    # Create test directory structure
    mkdir -p tests/{unit,integration}
    
    # Run tests
    uv run pytest tests/
    
    # Run with coverage
    uv run pytest --cov=src tests/
    ```

*   **Test Files Structure**:
    ```
    tests/
    ├── conftest.py              # Shared fixtures and configuration
    ├── pytest.ini              # Pytest configuration
    ├── unit/
    │   ├── test_utils.py        # Tests for utility functions
    │   ├── test_database.py     # Tests for database operations
    │   ├── test_etl_extract.py  # Tests for data extraction
    │   ├── test_etl_load.py     # Tests for data loading
    │   ├── test_etl_transform.py # Tests for data transformation
    │   └── test_ai_gemini.py    # Tests for AI processing
    └── integration/
        └── test_pipeline.py     # End-to-end pipeline tests
    ```

---
*This README was generated by an AI assistant.*