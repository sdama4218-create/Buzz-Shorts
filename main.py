import os
import googleapiclient.discovery
import googleapiclient.http
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

# 1. جلب البيانات من GitHub Secrets
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('GOOGLE_REFRESH_TOKEN')
API_KEY = os.environ.get('GOOGLE_API_KEY')

def create_sample_video(output_filename):
    """دالة لإنشاء فيديو بسيط للتجربة"""
    print("جاري إنشاء الفيديو...")
    try:
        # إنشاء خلفية سوداء لمدة 5 ثوانٍ بمقاس Shorts (1080x1920)
        bg = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=5)
        
        # إضافة نص في منتصف الفيديو
        txt = TextClip("Viral AI Content", fontsize=70, color='white', font='Arial')
        txt = txt.set_position('center').set_duration(5)
        
        # دمج النص مع الخلفية
        video = CompositeVideoClip([bg, txt])
        
        # حفظ الملف
        video.write_videofile(output_filename, fps=24)
        print(f"تم إنشاء الملف بنجاح: {output_filename}")
    except Exception as e:
        print(f"فشل إنشاء الفيديو: {e}")

def get_youtube_client():
    """الاتصال بيوتيوب"""
    creds = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    if not creds.valid:
        creds.refresh(Request())
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def upload_video(youtube, file_path, title, description):
    """رفع الفيديو"""
    request_body = {
        "snippet": {
            "categoryId": "22", 
            "title": title,
            "description": description,
            "tags": ["AI", "Shorts", "Automation"]
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    media_file = googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file)
    
    print(f"جاري رفع الفيديو إلى يوتيوب...")
    response = request.execute()
    print(f"✅ تم الرفع! الرابط: https://youtu.be/{response['id']}")

if __name__ == "__main__":
    VIDEO_FILE = "output_video.mp4" 
    
    # أولاً: نصنع الفيديو
    create_sample_video(VIDEO_FILE)
    
    # ثانياً: إذا تم صنع الفيديو بنجاح، نقوم برفعه
    if os.path.exists(VIDEO_FILE):
        try:
            youtube_client = get_youtube_client()
            upload_video(
                youtube_client, 
                VIDEO_FILE, 
                "فيديو مبرمج تلقائياً 🚀", 
                "هذا الفيديو تم إنشاؤه ورفعه بواسطة بوت خاص عبر GitHub Actions."
            )
        except Exception as e:
            print(f"حدث خطأ أثناء الرفع: {e}")
    else:
        print("خطأ: تعذر العثور على ملف الفيديو بعد محاولة إنشائه.")
        
