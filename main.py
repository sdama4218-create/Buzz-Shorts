import os
import asyncio
import edge_tts
from moviepy.editor import ColorClip, AudioFileClip

async def make_first_video():
    # إنشاء صوت تأكيد التشغيل بنجاح
    msg = "تم تفعيل البوت بنجاح! هذا هو أول فيديو يتم إنتاجه آلياً عبر جيث هب."
    communicate = edge_tts.Communicate(msg, "ar-SA-ZariyahNeural")
    await communicate.save("voice.mp3")
    
    # صناعة الفيديو (بصيغة Shorts)
    audio = AudioFileClip("voice.mp3")
    bg = ColorClip(size=(1080, 1920), color=(20, 20, 20)).set_duration(audio.duration)
    video = bg.set_audio(audio)
    video.write_videofile("first_test.mp4", fps=24, codec="libx264")
    print("Video Created: first_test.mp4")

if __name__ == "__main__":
    asyncio.run(make_first_video())
  
