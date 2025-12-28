"""History and shortlist routes for the Product Review Engine API."""

import re
from typing import Optional, List, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from db_models import User, AnalyzedProduct, ChatSession, ChatMessage, ShortlistedProduct

# Configuration constants
MAX_HISTORY_ITEMS = 20

router = APIRouter(prefix="/api", tags=["history"])


class HistoryReviewRequest(BaseModel):
    product_name: str


class HistoryProductItem(BaseModel):
    id: int
    product_name: str
    last_viewed_at: str
    rating: Optional[str] = None
    price: Optional[Any] = None


class HistoryChatSessionItem(BaseModel):
    id: int
    product_name: str
    created_at: str


class HistorySummaryRequest(BaseModel):
    user_id: Optional[str] = None


class HistorySummaryResponse(BaseModel):
    products: List[HistoryProductItem]
    sessions: List[HistoryChatSessionItem]


class ChatHistoryRequest(BaseModel):
    user_id: Optional[str] = None
    session_id: int


class LatestSessionRequest(BaseModel):
    user_id: Optional[str] = None
    product_name: str


class LatestSessionResponse(BaseModel):
    session_id: Optional[int]


class ShortlistItem(BaseModel):
    product_name: str
    created_at: str


class ShortlistAddRequest(BaseModel):
    product_name: str


class ShortlistRemoveRequest(BaseModel):
    product_name: str


def normalize_product_name(name: str) -> str:
    """Normalize product names for comparisons."""
    return re.sub(r"\s+", " ", (name or "").strip().lower())


@router.post("/history/review")
async def get_saved_review(
    req: HistoryReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = (
        db.query(AnalyzedProduct)
        .filter(
            AnalyzedProduct.user_id == current_user.id,
            AnalyzedProduct.product_name == req.product_name,
        )
        .first()
    )
    return {"review": obj.last_review_json if obj and obj.last_review_json else None}


@router.get("/shortlist", response_model=List[ShortlistItem])
async def get_shortlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(ShortlistedProduct)
        .filter(ShortlistedProduct.user_id == current_user.id)
        .order_by(ShortlistedProduct.created_at.desc())
        .all()
    )
    return [
        ShortlistItem(
            product_name=r.product_name,
            created_at=r.created_at.isoformat(),
        )
        for r in rows
    ]


@router.post("/shortlist/add")
async def add_to_shortlist(
    req: ShortlistAddRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    target = normalize_product_name(req.product_name)

    existing = (
        db.query(ShortlistedProduct)
        .filter(
            ShortlistedProduct.user_id == current_user.id,
            func.lower(ShortlistedProduct.product_name) == target.lower()
        )
        .first()
    )
    if existing:
        return {"ok": True, "message": "Already in shortlist"}

    row = ShortlistedProduct(user_id=current_user.id, product_name=req.product_name)
    db.add(row)
    db.commit()
    return {"ok": True, "message": "Added to shortlist"}


@router.post("/shortlist/remove")
async def remove_from_shortlist(
    req: ShortlistRemoveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    target = normalize_product_name(req.product_name)

    db.query(ShortlistedProduct).filter(
        ShortlistedProduct.user_id == current_user.id,
        func.lower(ShortlistedProduct.product_name) == target.lower()
    ).delete(synchronize_session=False)

    db.commit()
    return {"ok": True}


@router.post("/history/summary", response_model=HistorySummaryResponse)
async def get_history_summary(
    req: HistorySummaryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product_rows = (
        db.query(AnalyzedProduct)
        .filter(AnalyzedProduct.user_id == current_user.id)
        .order_by(AnalyzedProduct.last_viewed_at.desc())
        .limit(MAX_HISTORY_ITEMS)
        .all()
    )

    session_rows = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.created_at.desc())
        .limit(MAX_HISTORY_ITEMS)
        .all()
    )

    products: List[HistoryProductItem] = []
    for p in product_rows:
        rating = None
        price = None
        if p.last_review_json:
            rating = p.last_review_json.get("predicted_rating")
            price = p.last_review_json.get("price_naira") or p.last_review_json.get("price_info")

        products.append(
            HistoryProductItem(
                id=p.id,
                product_name=p.product_name,
                last_viewed_at=p.last_viewed_at.isoformat(),
                rating=rating,
                price=price,
            )
        )

    sessions = [
        HistoryChatSessionItem(
            id=s.id,
            product_name=s.product_name,
            created_at=s.created_at.isoformat(),
        )
        for s in session_rows
    ]

    return HistorySummaryResponse(products=products, sessions=sessions)


@router.post("/history/chat-session")
async def get_chat_session_messages(
    req: ChatHistoryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == req.session_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if not session:
        return {"messages": []}

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    return {
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ]
    }


@router.post("/history/latest-session", response_model=LatestSessionResponse)
async def get_latest_session(
    req: LatestSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == current_user.id, ChatSession.product_name == req.product_name)
        .order_by(ChatSession.created_at.desc())
        .first()
    )
    return LatestSessionResponse(session_id=session.id if session else None)
