import os
import random

# محاولة الاستدعاء بأكثر من طريقة لضمان عدم ظهور الخطأ مرة أخرى
try:
    from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
except ImportError:
    from moviepy.video.VideoClip import ColorClip, TextClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

def create_viral_video():
    try:
        print("بدء صناعة الفيديو...")
        quotes = ["Success needs action.", "Stay hungry, stay foolish.", "Dream big, work hard."]
        text_content = random.choice(quotes)
        
        # إنشاء الفيديو
        bg = ColorClip(size=(720, 1280), color=(0, 0, 0), duration=5) # صغرنا الحجم للسرعة
        
        # ملاحظة: إذا استمر خطأ TextClip، سنحول الفيديو لخلفية ملونة فقط للتأكد من الرفع
        try:
            txt = TextClip(text_content, fontsize=50, color='white', size=(600, None), method='caption')
            txt = txt.set_position('center').set_duration(5)
            final = CompositeVideoClip([bg, txt])
        except Exception as e:
            print(f"تحذير في النص: {e}. سيتم إنشاء فيديو ملون سادة للتجربة.")
            final = bg

        final.write_videofile("result.mp4", fps=24, codec="libx264", audio=False)
        return True
    except Exception as e:
        print(f"خطأ: {e}")
        return False

if __name__ == "__main__":
    create_viral_video()
    
