# database/models.py

class TableHeaders:
    CAMP = ["Camp_ID", "Camp_Name", "Detail", "Event_Date", "Location", "Price", "capacity", "User_ID", "Status"]
    USERS = ["User_ID", "Name", "Email", "Password_Hash", "Role"]
    BOOKING = ["Booking_ID", "User_ID", "Camp_ID", "Date", "Status", "amount", "Payment_method"]
    PAYMENTS = ["Payment_ID", "Booking_ID", "Amount", "Payment_method", "paid_at", "Status"]