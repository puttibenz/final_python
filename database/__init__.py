# database/__init__.py
from .connection import get_db_connection
from .init_db import init_database
from .crud import DatabaseCRUD

def setup_database():
    """ฟังก์ชันศูนย์กลางสำหรับเชื่อมต่อ เซ็ตอัป และคืนค่า CRUD"""
    sh = get_db_connection()
    init_database(sh)
    db = DatabaseCRUD(sh)
    return db