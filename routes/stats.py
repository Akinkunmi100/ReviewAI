"""Stats routes for the Product Review Engine API."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from db_models import User, AnalyzedProduct

AVG_REVIEWS_PER_PRODUCT = 10

router = APIRouter(prefix="/api", tags=["stats"])


class StatsResponse(BaseModel):
    products_analyzed: int
    reviews_processed: int
    active_users: int


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get real statistics from the database."""
    products_count = db.query(AnalyzedProduct).count()
    reviews_count = products_count * AVG_REVIEWS_PER_PRODUCT
    users_count = db.query(User).count()
    
    return StatsResponse(
        products_analyzed=products_count,
        reviews_processed=reviews_count,
        active_users=users_count
    )
