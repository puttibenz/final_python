import json
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

load_dotenv()

# 1. API Configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_batch_with_gemini(posts_batch):
    """
    Sends a batch of posts to Gemini to extract information in one call.
    """
    # Create a numbered list of posts for the prompt
    batch_text = ""
    for i, post in enumerate(posts_batch):
        batch_text += f"--- POST {i+1} ---\n{post.get('text', '')}\n\n"

    prompt = f"""
    คุณคือผู้ช่วยจัดการข้อมูลทริปและแคมป์ หน้าที่ของคุณคืออ่านลิสต์ของโพสต์ Facebook ต่อไปนี้:
    
    {batch_text}

    สำหรับแต่ละโพสต์ ให้วิเคราะห์ดังนี้:
    1. วิเคราะห์ว่าเป็น "ประกาศรับสมัคร/ชวนไปทริปหรือแคมป์" หรือไม่ (is_camp_post: true/false)
    2. ถ้าใช่ให้สกัดข้อมูลตามโครงสร้างที่กำหนด ถ้าหาไม่เจอให้ใส่ "" หรือ 0
    
    สำคัญ: ต้องตอบกลับเป็น JSON ARRAY ของออบเจกต์ จำนวน {len(posts_batch)} รายการ ตามลำดับโพสต์ที่ส่งไป
    โครงสร้างออบเจกต์ใน Array:
    {{
        "is_camp_post": true หรือ false,
        "name": "ชื่อทริป (สรุปสั้นๆ)",
        "start_date": "วันที่จัดกิจกรรม",
        "duration": "จำนวนวัน (ตัวเลข)",
        "location": "สถานที่ หรือ จังหวัด",
        "price": "ราคาค่าใช้จ่าย",
        "slots": "จำนวนคนรับสมัคร (ตัวเลข)",
        "contact": "ช่องทางติดต่อ",
        "link": "ลิงก์"
    }}
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"❌ Error during API call: {e}")
        return None

def main():
    input_filename = 'apify_raw_data.json'
    output_filename = 'clean_camps_ready_for_sql.json'
    batch_size = 10  # Process 10 posts per 1 API call
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            apify_posts = json.load(f)
    except FileNotFoundError:
        print(f"❌ หาไฟล์ {input_filename} ไม่เจอ")
        return

    # Filter posts that have text
    valid_posts = [p for p in apify_posts if p.get('text')]
    
    # Process up to 200 posts (20 batches of 10)
    limit_posts = valid_posts[:200]
    clean_camps = []

    print(f"เจอข้อมูลที่มีข้อความ {len(valid_posts)} โพสต์")
    print(f"กำลังเริ่มประมวลผล {len(limit_posts)} โพสต์ (แบ่งเป็น {len(limit_posts)//batch_size} batches)...\n")

    for i in range(0, len(limit_posts), batch_size):
        batch = limit_posts[i:i + batch_size]
        current_batch_num = (i // batch_size) + 1
        print(f"📦 กำลังประมวลผล Batch ที่ {current_batch_num} ({i+1} ถึง {min(i+batch_size, len(limit_posts))})...")
        
        extracted_results = extract_batch_with_gemini(batch) 
        
        if extracted_results and isinstance(extracted_results, list):
            for index, data in enumerate(extracted_results):
                if data.get("is_camp_post") == True:
                    # Add metadata from the original post
                    original_post = batch[index]
                    data['facebook_link'] = original_post.get('facebookUrl', original_post.get('url', ''))
                    data['source'] = 'apify_facebook'
                    clean_camps.append(data)
            
            print(f"✅ Batch {current_batch_num} เสร็จสิ้น. (เจอทริปสะสม: {len(clean_camps)})")
        else:
            print(f"⚠️ Batch {current_batch_num} ล้มเหลวหรือได้ข้อมูลไม่ถูกต้อง")

        # Save every batch
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(clean_camps, f, ensure_ascii=False, indent=2)
            
        # Respect Rate Limits (15 RPM) -> wait 15 seconds between batches
        time.sleep(15)

    print(f"\n🎉 เสร็จสิ้น! บันทึกข้อมูล {len(clean_camps)} ทริปลงไฟล์ {output_filename} แล้ว")

if __name__ == "__main__":
    main()
