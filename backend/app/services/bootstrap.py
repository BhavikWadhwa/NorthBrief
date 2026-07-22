from sqlalchemy.orm import Session

from app.models import Category, Region
from app.services.constants import CATEGORY_DEFINITIONS, REGION_DEFINITIONS


def ensure_static_data(db: Session) -> None:
    existing_categories = {item.code for item in db.query(Category).all()}
    for category in CATEGORY_DEFINITIONS:
        if category["code"] not in existing_categories:
            db.add(Category(code=category["code"], label=category["label"]))

    existing_regions = {item.code for item in db.query(Region).all()}
    for region in REGION_DEFINITIONS:
        if region["code"] not in existing_regions:
            db.add(
                Region(
                    code=region["code"],
                    name=region["name"],
                    region_type=region["region_type"],
                    parent_code=region["parent_code"],
                )
            )

    db.commit()

