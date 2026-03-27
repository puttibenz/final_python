from typing import List, Optional
from datetime import datetime, timedelta
from .models import User, Booking, Camp
import random

# Mock data for demonstration
mock_users = [
    User(
        id=1,
        username="admin",
        email="admin@example.com",
        full_name="Administrator",
        phone="+66 123 456 789",
        created_at=datetime(2024, 1, 1),
        total_bookings=5,
        total_spent=25000.0
    )
]


mock_camps = [
    Camp(id=1, name="Mountain View Camp", location="Chiang Mai", price_per_night=1500.0, max_guests=4, description="Beautiful mountain views"),
    Camp(id=2, name="Beach Paradise", location="Phuket", price_per_night=2000.0, max_guests=6, description="Seaside camping"),
    Camp(id=3, name="Forest Retreat", location="Kanchanaburi", price_per_night=1200.0, max_guests=2, description="Peaceful forest setting"),
]

mock_bookings = [
    Booking(
        id=1,
        user_id=1,
        camp_name="Mountain View Camp",
        location="Chiang Mai",
        check_in_date=datetime(2024, 3, 1),
        check_out_date=datetime(2024, 3, 3),
        guests=2,
        total_price=3000.0,
        status="completed",
        created_at=datetime(2024, 2, 25)
    ),
    Booking(
        id=2,
        user_id=1,
        camp_name="Beach Paradise",
        location="Phuket",
        check_in_date=datetime(2024, 4, 15),
        check_out_date=datetime(2024, 4, 18),
        guests=4,
        total_price=6000.0,
        status="confirmed",
        created_at=datetime(2024, 3, 20)
    ),
    Booking(
        id=3,
        user_id=1,
        camp_name="Forest Retreat",
        location="Kanchanaburi",
        check_in_date=datetime(2024, 2, 10),
        check_out_date=datetime(2024, 2, 12),
        guests=1,
        total_price=2400.0,
        status="cancelled",
        created_at=datetime(2024, 2, 5)
    ),
]

def get_user_by_username(username: str) -> Optional[User]:
    """Get user by username"""
    for user in mock_users:
        if user.username == username:
            return user
    return None

def get_user_bookings(user_id: int) -> List[Booking]:
    """Get all bookings for a user"""
    return [booking for booking in mock_bookings if booking.user_id == user_id]

def get_user_stats(user_id: int) -> dict:
    """Get user statistics"""
    bookings = get_user_bookings(user_id)
    total_bookings = len(bookings)
    completed_bookings = len([b for b in bookings if b.status == "completed"])
    cancelled_bookings = len([b for b in bookings if b.status == "cancelled"])
    total_spent = sum(b.total_price for b in bookings if b.status == "completed")

    return {
        "total_bookings": total_bookings,
        "completed_bookings": completed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_spent": total_spent,
        "average_booking_value": total_spent / completed_bookings if completed_bookings > 0 else 0,
        "favorite_location": get_favorite_location(bookings)
    }

def get_favorite_location(bookings: List[Booking]) -> str:
    """Get user's favorite camping location"""
    locations = {}
    for booking in bookings:
        if booking.status == "completed":
            locations[booking.location] = locations.get(booking.location, 0) + 1

    if locations:
        return max(locations, key=locations.get)
    return "None"