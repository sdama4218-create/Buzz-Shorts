import os
import random
import googleapiclient.discovery
import googleapiclient.http
from google.oauth2.credentials import Credentials
# محاولة استدعاء مكتبات الفيديو
try:
    from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
except ImportError:
    from moviepy.video.VideoClip import ColorClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- أولاً: دالة الرفع التلقائي ---
def upload_to_youtube(video_path):
    print("بدء الرفع التلقائي إلى يوتيوب...")
    try:
        # استدعاء البيانات من السكرت (Secrets)
        creds = Credentials(
            None,
            refresh_token=os.environ.get('GOOGLE_REFRESH_TOKEN'),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ.get('GOOGLE_CLIENT_ID'),
            client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        )
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "categoryId": "22",
                    "description": "فيديو مرفوع تلقائياً بواسطة السكربت",
                    "title": f"فيديو جديد {random.randint(100, 999)}"
                },
                "status": {"privacyStatus": "public"}
            },
            media_body=googleapiclient.http.MediaFileUpload(video_path, chunksize=-1, resumable=True)
        )
        response = request.execute()
        print(f"تم الرفع بنجاح! رابط الفيديو: https://youtu.be/{response['id']}")
    except Exception as e:
        print(f"فشل الرفع التلقائي: {e}")

# --- ثانياً: دالة صناعة الفيديو ---
def create_viral_video():
    output_file = "result.mp4"
    try:
        print("جاري إنشاء الفيديو...")
        bg = ColorClip(size=(720, 1280), color=(random.randint(0,200), 40, 80), duration=5)
        # هنا يتم حفظ الفيديو
        bg.write_videofile(output_file, fps=24, codec="libx264", audio=False)
        
        if os.path.exists(output_file):
            print("الفيديو جاهز.")
            # استدعاء الرفع التلقائي فوراً
            upload_to_youtube(output_file)
        else:
            print("لم يتم العثور على الملف.")
    except Exception as e:
        print(f"خطأ في الصناعة: {e}")

if __name__ == "__main__":
    create_viral_video()
    
