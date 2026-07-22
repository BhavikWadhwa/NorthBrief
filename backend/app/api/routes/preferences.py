from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User, UserPreference
from app.schemas import PreferenceUpdate

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.get("", response_model=PreferenceUpdate)
def get_preferences(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> PreferenceUpdate:
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return PreferenceUpdate(
        country=pref.country,
        province=pref.province,
        city=pref.city,
        category_codes=pref.category_codes,
        local_global_weight=pref.local_global_weight,
        finance_weight=pref.finance_weight,
        skip_personalization=pref.skip_personalization,
    )


@router.put("", response_model=PreferenceUpdate)
def update_preferences(
    payload: PreferenceUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> PreferenceUpdate:
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    if not pref:
        pref = UserPreference(user_id=current_user.id)
        db.add(pref)
    pref.country = payload.country
    pref.province = payload.province
    pref.city = payload.city
    pref.category_codes = payload.category_codes
    pref.local_global_weight = payload.local_global_weight
    pref.finance_weight = payload.finance_weight
    pref.skip_personalization = payload.skip_personalization
    db.commit()
    return payload

