"""Review and comparison routes for the Product Review Engine API."""

import logging
import re
from typing import Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, conlist
from sqlalchemy.orm import Session

from auth import get_current_user_optional
from database import get_db
from db_models import User, AnalyzedProduct
from routes._service import get_review_service, ProductReviewError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["review"])


class ReviewRequest(BaseModel):
    product_name: str
    data_mode: Optional[str] = None
    use_web: bool = True
    user_id: Optional[str] = None
    
    @property
    def validated_product_name(self) -> str:
        """Return sanitized product name."""
        name = self.product_name.strip()
        if not name or len(name) > 200:
            raise ValueError("Product name must be between 1 and 200 characters")
        name = re.sub(r'[<>"\'\\\/]', '', name)
        return name


class CompareRequest(BaseModel):
    products: conlist(str, min_length=2, max_length=4)


def record_analyzed_product(db: Session, user: User, product_name: str, review_json: Dict[str, Any]) -> None:
    from datetime import datetime, timezone

    safe_review_json = jsonable_encoder(review_json)

    obj = (
        db.query(AnalyzedProduct)
        .filter(AnalyzedProduct.user_id == user.id, AnalyzedProduct.product_name == product_name)
        .first()
    )
    if obj:
        obj.last_review_json = safe_review_json
        obj.last_viewed_at = datetime.now(timezone.utc)
    else:
        obj = AnalyzedProduct(
            user_id=user.id,
            product_name=product_name,
            last_review_json=safe_review_json,
        )
        db.add(obj)
    db.commit()


@router.post("/review")
async def generate_review(
    req: ReviewRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Generate an enhanced product review as JSON."""
    service = get_review_service()
    try:
        product_name = req.validated_product_name
        review = service.generate_review(product_name, use_web_search=req.use_web, mode=req.data_mode)

        if current_user:
            if hasattr(review, "model_dump"):
                review_dict = review.model_dump()
            elif hasattr(review, "dict"):
                review_dict = review.dict()
            else:
                review_dict = review
            record_analyzed_product(db, current_user, product_name, review_dict)

        return review
    except ValueError as e:
        logger.warning(f"Validation error in review: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ProductReviewError as e:
        logger.warning(f"Product review error: {e}")
        return {"error": {"message": str(e)}}
    except Exception as e:
        logger.error(f"Unexpected error in review endpoint: {e}", exc_info=True)
        return {"error": {"message": "An unexpected error occurred while processing your request."}}


@router.post("/compare")
async def compare_products(req: CompareRequest):
    """Generate a side-by-side comparison between up to 3 products."""
    service = get_review_service()
    try:
        comparison = service.generate_comparison(req.products)
        return comparison
    except ProductReviewError as e:
        logger.warning(f"Product review error in compare: {e}")
        return {"error": {"message": str(e)}}
    except Exception as e:
        logger.error(f"Unexpected error in compare endpoint: {e}", exc_info=True)
        return {"error": {"message": "An unexpected error occurred while comparing products."}}
