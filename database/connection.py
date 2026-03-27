import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """สร้าง connection ไปยัง MySQL (XAMPP)"""
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "camping_db"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print(f"❌ MySQL Connection Error: {e}")
        return None
