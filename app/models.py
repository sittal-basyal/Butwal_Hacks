from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class BookMode(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    DONATE = "donate"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    books = relationship("Book", back_populates="seller")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String)
    price = Column(Float, default=0.0)
    mode = Column(SQLEnum(BookMode))
    image_filename = Column(String, nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    address_label = Column(String, nullable=True)
    seller_id = Column(Integer, ForeignKey("users.id"))
    contact_number = Column(String, nullable=True)
    ai_summary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    seller = relationship("User", back_populates="books")
