import bcrypt
import uuid

def hash_password(password: str) -> str:
    """เข้ารหัสผ่านด้วย bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ตรวจสอบรหัสผ่านว่าตรงกับ Hash ในระบบหรือไม่"""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        # ดักจับ Error กรณีข้อมูลใน Google Sheets เป็นข้อความธรรมดา (ไม่ใช่ Hash)
        return False

def check_email_exists(db, email: str) -> bool:
    """ตรวจสอบว่ามีอีเมลนี้ในระบบแล้วหรือไม่"""
    users = db.get_all_users()
    for user in users[1:]: # ข้ามหัวตาราง
        if len(user) > 2 and user[2] == email:
            return True
    return False

def register_new_user(db, name: str, email: str, password: str, role: str = "User") -> tuple:
    """สร้างบัญชีผู้ใช้ใหม่"""
    if check_email_exists(db, email):
        return False, "อีเมลนี้ถูกใช้งานแล้ว"
    
    hashed_password = hash_password(password)
    user_id = f"U-{uuid.uuid4().hex[:8].upper()}"
    new_user_data = [user_id, name, email, hashed_password, role]
    
    if db.add_new_user(new_user_data):
        return True, "สมัครสมาชิกสำเร็จ!"
    return False, "เกิดข้อผิดพลาดในการบันทึกข้อมูล"

def login_user(db, email: str, password: str) -> tuple:
    """ตรวจสอบอีเมลและรหัสผ่านสำหรับเข้าสู่ระบบ"""
    users = db.get_all_users()
    
    for user in users[1:]:
        # เช็กว่าแถวมีข้อมูลครบ และอีเมลตรงกัน
        if len(user) > 4 and user[2] == email:
            hashed_pw = user[3] 
            
            if verify_password(password, hashed_pw):
                user_data = {
                    "User_ID": user[0],
                    "Name": user[1],
                    "Email": user[2],
                    "Role": user[4]
                }
                return True, user_data
            else:
                return False, "รหัสผ่านไม่ถูกต้อง"
                
    return False, "ไม่พบอีเมลนี้ในระบบ"