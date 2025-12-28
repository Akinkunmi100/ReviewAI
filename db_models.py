from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    JSON,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # Historically this project used an external string id.
    # For full login, we treat this as the user's email (unique).
    external_id = Column(String(255), unique=True, index=True, nullable=False)

    # Password hash for email/password login. Nullable to avoid breaking existing DBs.
    password_hash = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    chat_sessions = relationship("ChatSession", back_populates="user")
    analyzed_products = relationship("AnalyzedProduct", back_populates="user")
    profile = relationship("UserProfileData", back_populates="user", uselist=False)


class UserProfileData(Base):
    """Persisted user profile with preferences for personalized recommendations."""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    min_budget = Column(Integer, nullable=True)
    max_budget = Column(Integer, nullable=True)
    use_cases = Column(JSON, default=[])
    preferred_brands = Column(JSON, default=[])
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="profile")


class AnalyzedProduct(Base):
    __tablename__ = "analyzed_products"
    __table_args__ = (
        UniqueConstraint("user_id", "product_name", name="uq_user_product"),
        # Composite index for efficient history queries (user_id filter + last_viewed_at sort)
        Index("ix_analyzed_products_user_viewed", "user_id", "last_viewed_at"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_name = Column(String(512), index=True, nullable=False)
    last_review_json = Column(JSON, nullable=True)
    last_viewed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", back_populates="analyzed_products")


class ShortlistedProduct(Base):
    __tablename__ = "shortlisted_products"
    __table_args__ = (
        UniqueConstraint("user_id", "product_name", name="uq_user_shortlist"),
        # Index for efficient shortlist queries sorted by date
        Index("ix_shortlist_user_created", "user_id", "created_at"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_name = Column(String(512), index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User")


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    __table_args__ = (
        # Composite index for efficient session history queries
        Index("ix_chat_sessions_user_created", "user_id", "created_at"),
        # Index for finding latest session by user and product
        Index("ix_chat_sessions_user_product", "user_id", "product_name"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_name = Column(String(512), index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    session = relationship("ChatSession", back_populates="messages")
