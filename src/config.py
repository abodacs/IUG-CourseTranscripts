import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")
BUCKET_NAME = os.environ.get("bucket_name")
AWS_ACCESS_KEY_ID = os.environ.get("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = os.environ.get("aws_secret_access_key")
ENDPOINT_URL = os.environ.get("endpoint_url")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Constants
DB_PATH = "youtube-iug.db"
CHUNK_SIZE = 222
POSTFIX = "_postprocess"
