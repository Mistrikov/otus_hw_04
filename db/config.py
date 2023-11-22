from pathlib import Path

from sqlalchemy import create_engine

BASE_DIR = Path(__file__).parent.parent
db_file_path = BASE_DIR / "blog.sqlite3"

DB_URL = f"sqlite:///{db_file_path}"
# DB_URL = "postgresql+pg8000://user:example@localhost:5432/blog"

DB_ECHO = True

engine = create_engine(
    url=DB_URL,
    echo=DB_ECHO,
)