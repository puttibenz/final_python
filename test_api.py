import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# ใส่ API Key ของคุณ
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("รายชื่อโมเดลที่คุณสามารถใช้ได้:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)