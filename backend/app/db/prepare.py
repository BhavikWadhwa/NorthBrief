import re

from sqlalchemy import create_engine, text

from app.core.config import get_settings

VALID_SCHEMA = re.compile(r"^[a-z][a-z0-9_]{0,62}$")


def prepare_database_schema() -> None:
    settings = get_settings()
    schema = settings.database_schema
    if not schema:
        return
    if not VALID_SCHEMA.fullmatch(schema):
        raise ValueError("DB_SCHEMA must be a lowercase PostgreSQL identifier")

    engine = create_engine(settings.normalized_database_url, pool_pre_ping=True)
    try:
        with engine.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    finally:
        engine.dispose()


if __name__ == "__main__":
    prepare_database_schema()
