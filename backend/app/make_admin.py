import sys

from app.db.session import SessionLocal
from app.models import User


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python -m app.make_admin <email>")
    email = sys.argv[1].strip().lower()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise SystemExit(f"User not found: {email}")
        user.is_admin = True
        db.commit()
        print(f"Promoted to admin: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

