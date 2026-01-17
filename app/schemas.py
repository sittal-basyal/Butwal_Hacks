
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class BookMode(str, Enum):
    BUY = "buy"
    SELL = "sell"
    DONATE = "donate"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    price: float = 0.0
    mode: BookMode
    latitude: Optional[float] = None
    longitude: Optional[float] = None


BookCreate = BookBase

class BookResponse(BookBase):
    id: int
    seller_id: int
    created_at: Optional[datetime] = None
    
    image_filename: Optional[str] = None
    address_label: Optional[str] = None
    seller_name: Optional[str] = None
    contact_number: Optional[str] = None 
    ai_summary: Optional[str] = None
    distance_meters: Optional[float] = None 

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)