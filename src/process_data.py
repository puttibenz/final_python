import json
import google.generativeai as genai
import time
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiDataProcessor:
    def __init__(self, api_key=None, model_name='gemini-2.0-flash'):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.clean_camps = []

    def _extract_batch_with_gemini(self, posts_batch):
        """Sends a batch of posts to Gemini to extract information in one call."""
        batch_data = []
        for i, post in enumerate(posts_batch):
            batch_data.append({
                "id": i + 1,
                "text": post.get('text', ''),
                "url": post.get('facebookUrl', post.get('url', ''))
            })

        prompt = f"""
        คุณคือผู้ช่วยจัดการข้อมูลทริปและแคมป์ หน้าที่ของคุณคือวิเคราะห์ลิสต์ของโพสต์ Facebook ต่อไปนี้ (ในรูปแบบ JSON):
        
        {json.dumps(batch_data, ensure_ascii=False, indent=2)}

        สำหรับแต่ละโพสต์ ให้วิเคราะห์ดังนี้:
        1. วิเคราะห์ว่าเป็น "ประกาศรับสมัคร/ชวนไปทริปหรือแคมป์" หรือไม่ (is_camp_post: true/false)
        2. ถ้าใช่ให้สกัดข้อมูลตามโครงสร้างที่กำหนด ถ้าหาไม่เจอให้ใส่ "" หรือ 0
        
        สำคัญ: ต้องตอบกลับเป็น JSON ARRAY ของออบเจกต์ จำนวน {len(posts_batch)} รายการ ตามลำดับ id ที่ส่งไป
        โครงสร้างออบเจกต์ในแต่ละรายการ:
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
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(response_mime_type="application/json")
            )
            # Robustly handle potential markdown wrapping even with mime_type
            clean_text = response.text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text.replace("```json", "", 1).replace("```", "", 1).strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"❌ Error during API call: {e}")
            return None

    def process_data(self, input_filename='apify_raw_data.json', output_filename='clean_camps_ready_for_sql.json', batch_size=10, limit=200):
        """Orchestrates the data processing workflow."""
        try:
            with open(input_filename, 'r', encoding='utf-8') as f:
                apify_posts = json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: File {input_filename} not found.")
            return

        valid_posts = [p for p in apify_posts if p.get('text')]
        limit_posts = valid_posts[:limit]
        self.clean_camps = []

        print(f"📊 Found {len(valid_posts)} valid posts. Processing {len(limit_posts)} posts...")

        for i in range(0, len(limit_posts), batch_size):
            batch = limit_posts[i:i + batch_size]
            current_batch_num = (i // batch_size) + 1
            print(f"📦 Processing Batch {current_batch_num}...")
            
            extracted_results = self._extract_batch_with_gemini(batch) 
            
            if extracted_results and isinstance(extracted_results, list):
                for index, data in enumerate(extracted_results):
                    if data.get("is_camp_post") == True:
                        original_post = batch[index]
                        data['facebook_link'] = original_post.get('facebookUrl', original_post.get('url', ''))
                        data['source'] = 'apify_facebook'
                        self.clean_camps.append(data)
                
                print(f"✅ Batch {current_batch_num} done. (Total camps found: {len(self.clean_camps)})")
            else:
                print(f"⚠️ Batch {current_batch_num} failed or returned invalid data.")

            # Intermediate save
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(self.clean_camps, f, ensure_ascii=False, indent=2)
                
            # Rate limit respect
            time.sleep(15)

        print(f"\n🎉 Finished! Saved {len(self.clean_camps)} camps to {output_filename}")

if __name__ == "__main__":
    processor = GeminiDataProcessor()
    processor.process_data()
