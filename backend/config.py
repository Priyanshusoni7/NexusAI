import os
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote

# Base directory for the backend package
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from backend/.env explicitly
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)


def _sqlite_path_from_env() -> str:
    database_path = os.getenv("DATABASE_PATH")
    if database_path:
        if not os.path.isabs(database_path):
            return os.path.abspath(os.path.join(BASE_DIR, database_path))
        return database_path

    database_url = os.getenv("DATABASE_URL", "")
    if database_url.startswith("sqlite:///"):
        parsed = urlparse(database_url)
        path = unquote(parsed.path)
        if path.startswith("/") and len(path) > 2 and path[2] == ":":
            path = path[1:]
        elif path.startswith("/./") or path.startswith("/../"):
            path = path[1:]

        if path and not os.path.isabs(path):
            return os.path.abspath(os.path.join(BASE_DIR, path))
        return path or os.path.join(BASE_DIR, "nexus.db")

    return os.path.join(BASE_DIR, "nexus.db")


def _chroma_dir_from_env() -> str:
    chroma_dir = os.getenv("CHROMA_DB_DIR", "chroma_db")
    if not os.path.isabs(chroma_dir):
        return os.path.abspath(os.path.join(BASE_DIR, chroma_dir))
    return chroma_dir


class Settings:
    PROJECT_NAME: str = "NexusAI"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    DATABASE_PATH: str = _sqlite_path_from_env()
    CHROMA_DB_DIR: str = _chroma_dir_from_env()
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))


settings = Settings()
