import time

from app.db.session import SessionLocal
from app.services.bootstrap import ensure_static_data
from app.services.ingestion.pipeline import run_ingestion


def run_forever(interval_seconds: int = 900) -> None:
    while True:
        db = SessionLocal()
        try:
            ensure_static_data(db)
            run_ingestion(db, triggered_by="scheduler")
        finally:
            db.close()
        time.sleep(interval_seconds)


if __name__ == "__main__":
    run_forever()

