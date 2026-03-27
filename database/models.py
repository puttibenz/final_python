from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None
    created_at: datetime
    total_bookings: int = 0
    total_spent: float = 0.0

class Booking(BaseModel):
    id: int
    user_id: int
    camp_name: str
    location: str
    check_in_date: datetime
    check_out_date: datetime
    guests: int
    total_price: float
    status: str  # 'confirmed', 'cancelled', 'completed'
    created_at: datetime

class Camp(BaseModel):
    id: int
    name: str
    location: str
    price_per_night: float
    max_guests: int
    description: str