"""Profile routes for the Product Review Engine API."""

import logging
from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from db_models import User, UserProfileData

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["profile"])


class ProfileSaveRequest(BaseModel):
    user_id: Optional[str] = None
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None
    use_cases: List[str] = []
    preferred_brands: List[str] = []


class ProfileResponse(BaseModel):
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None
    use_cases: List[str] = []
    preferred_brands: List[str] = []


@router.post("/profile")
async def save_profile(
    req: ProfileSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Save or update user profile preferences. Requires authentication."""
    user = current_user

    profile = db.query(UserProfileData).filter(UserProfileData.user_id == user.id).first()
    
    if profile:
        profile.min_budget = req.min_budget
        profile.max_budget = req.max_budget
        profile.use_cases = req.use_cases
        profile.preferred_brands = req.preferred_brands
    else:
        profile = UserProfileData(
            user_id=user.id,
            min_budget=req.min_budget,
            max_budget=req.max_budget,
            use_cases=req.use_cases,
            preferred_brands=req.preferred_brands,
        )
        db.add(profile)
    
    db.commit()
    logger.info(f"Profile saved for user {user.external_id}")
    return {"status": "ok", "message": "Profile saved successfully"}


@router.get("/profile", response_model=Optional[ProfileResponse])
async def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get saved user profile preferences. Requires authentication."""
    profile = db.query(UserProfileData).filter(UserProfileData.user_id == current_user.id).first()
    if not profile:
        return None
    
    return ProfileResponse(
        min_budget=profile.min_budget,
        max_budget=profile.max_budget,
        use_cases=profile.use_cases or [],
        preferred_brands=profile.preferred_brands or [],
    )
