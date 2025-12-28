"""Chat routes for the Product Review Engine API."""

import logging
import re
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import get_current_user_optional
from database import get_db
from db_models import User, ChatSession, ChatMessage
from core.models import UserProfile
from routes._service import get_review_service, ProductReviewError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    product_name: str
    message: str
    conversation_history: List[Dict[str, str]] = []
    data_mode: Optional[str] = None
    use_web: bool = True
    user_profile: Optional[Dict[str, Any]] = None
    session_id: Optional[int] = None
    user_id: Optional[str] = None
    
    @property
    def validated_message(self) -> str:
        """Return sanitized chat message."""
        msg = self.message.strip()
        if not msg or len(msg) > 5000:
            raise ValueError("Message must be between 1 and 5000 characters")
        return msg
    
    @property
    def validated_product_name(self) -> str:
        """Return sanitized product name."""
        name = self.product_name.strip()
        if not name or len(name) > 200:
            raise ValueError("Product name must be between 1 and 200 characters")
        name = re.sub(r'[<>"\'\\\/]', '', name)
        return name


def create_or_get_chat_session(db: Session, user: User, product_name: str, session_id: Optional[int]) -> ChatSession:
    """Get existing session or create new one."""
    if session_id:
        session = (
            db.query(ChatSession)
            .filter(ChatSession.id == session_id, ChatSession.user_id == user.id)
            .first()
        )
        if session:
            return session
    
    session = ChatSession(user_id=user.id, product_name=product_name)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def save_chat_turn(db: Session, session: ChatSession, user_message: str, assistant_reply: str) -> None:
    db.add_all(
        [
            ChatMessage(session_id=session.id, role="user", content=user_message),
            ChatMessage(session_id=session.id, role="assistant", content=assistant_reply),
        ]
    )
    db.commit()


@router.post("/chat")
async def chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """Get a chat response about a product."""
    service = get_review_service()
    try:
        product_name = req.validated_product_name
        message = req.validated_message
        
        review = service.generate_review(product_name, use_web_search=req.use_web, mode=req.data_mode)

        profile_obj = None
        if req.user_profile:
            try:
                profile_obj = UserProfile(**req.user_profile)
            except Exception:
                profile_obj = None

        reply = service.chat_service.get_chat_response(
            user_message=message,
            conversation_history=req.conversation_history,
            product_review=review,
            user_profile=profile_obj,
        )

        session_id: Optional[int] = None
        if current_user:
            session = create_or_get_chat_session(db, current_user, product_name, req.session_id)
            save_chat_turn(db, session, message, reply)
            session_id = session.id

        return {"reply": reply, "session_id": session_id}
    except ProductReviewError as e:
        logger.warning(f"Product review error in chat: {e}")
        return {"error": {"message": str(e)}}
    except ValueError as e:
        logger.warning(f"Validation error in chat: {e}")
        return {"error": {"message": str(e)}}
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        return {"error": {"message": "An unexpected error occurred while processing your request."}}
