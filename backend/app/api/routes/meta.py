from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Category, Region

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)) -> dict:
    rows = db.query(Category).filter(Category.is_active.is_(True)).order_by(Category.label.asc()).all()
    return {"items": [{"code": row.code, "label": row.label} for row in rows]}


@router.get("/regions")
def list_regions(db: Session = Depends(get_db)) -> dict:
    rows = db.query(Region).filter(Region.is_active.is_(True)).order_by(Region.name.asc()).all()
    return {
        "items": [
            {
                "code": row.code,
                "name": row.name,
                "region_type": row.region_type,
                "parent_code": row.parent_code,
                "country": row.country,
            }
            for row in rows
        ]
    }

