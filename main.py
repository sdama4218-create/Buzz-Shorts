import os
import random
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

def create_viral_video():
    try:
        print("جاري إنشاء الفيديو الفيروسي...")
        quotes = [
            "Success is not final, failure is not fatal.",
            "Believe you can and you're halfway there.",
            "Do what you can, with what you have, where you are."
        ]
        text_content = random.choice(quotes)
        
        # إنشاء الخلفية
        bg = ColorClip(size=(1080, 1920), color=(20, 20, 20), duration=5)
        
        # إنشاء النص مع معالجة الأخطاء
        try:
            txt = TextClip(text_content, fontsize=70, color='white', size=(900, None), method='caption')
        except:
            # حل بديل إذا فشل ImageMagick في قراءة الخطوط المعقدة
            print("تحذير: مشكلة في الخط، يتم استخدام الإعدادات البسيطة")
            txt = TextClip(text_content, fontsize=70, color='white')

        txt = txt.set_position('center').set_duration(5)
        
        final = CompositeVideoClip([bg, txt])
        final.write_videofile("result.mp4", fps=24, codec="libx264", audio=False)
        print("تم حفظ الفيديو بنجاح باسم result.mp4")
        return True
    except Exception as e:
        print(f"خطأ كارثي في التصنيع: {e}")
        return False

if __name__ == "__main__":
    if create_viral_video():
        print("جاهز للرفع! الآن السيرفر سيرفع الفيديو فوراً.")
        
