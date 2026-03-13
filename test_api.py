import google.generativeai as genai

# ใส่ API Key ของคุณ
genai.configure(api_key="AIzaSyDoynTfcXBsYb51Myd8z9_vZ3XTQ1Uz6hg")

print("รายชื่อโมเดลที่คุณสามารถใช้ได้:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)