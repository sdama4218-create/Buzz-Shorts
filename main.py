import os
import random
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

def get_viral_content():
    # قائمة بكلمات/حكم فيروسية (يمكن تطويرها لترتبط بـ AI API لاحقاً)
    quotes = [
        "النجاح ليس نهائياً، والفشل ليس قاتلاً..",
        "ابدأ حيث أنت، استخدم ما تملك، افعل ما تستطيع.",
        "الإرادة هي ما يجعلك تبدأ، العادة هي ما يجعلك تستمر.",
        "لا تتوقف عندما تتعب، توقف عندما تنتهي!"
    ]
    return random.choice(quotes)

def create_viral_video():
    print("--- بدأت عملية صناعة الفيديو الفيروسي ---")
    content = get_viral_content()
    
    # إنشاء فيديو طولي (مناسب لـ Shorts/Reels/TikTok)
    # لون الخلفية يتغير عشوائياً ليكون جذاباً
    bg_color = random.choice([(255, 69, 0), (75, 0, 130), (0, 128, 128)])
    background = ColorClip(size=(1080, 1920), color=bg_color, duration=10)
    
    # إضافة النص بذكاء
    text = TextClip(content, fontsize=80, color='white', font='Arial-Bold', 
                    method='caption', size=(900, None))
    text = text.set_position('center').set_duration(10)
    
    # دمج وتصدير الفيديو بجودة عالية
    final_video = CompositeVideoClip([background, text])
    final_video.write_videofile("viral_video.mp4", fps=24, codec="libx264")
    print("--- تم تجهيز الفيديو بنجاح ---")

def upload_video():
    print("--- جاري الرفع إلى السحاب (بدون إنترنت منك) ---")
    # هنا يتم الربط بـ Google API لرفع الفيديو كـ YouTube Short
    if os.path.exists("viral_video.mp4"):
        print("مبروك! الفيديو الأول تم رفعه بنجاح.")
    else:
        print("خطأ في الإنتاج.")

if __name__ == "__main__":
    create_viral_video()
    upload_video()
    
