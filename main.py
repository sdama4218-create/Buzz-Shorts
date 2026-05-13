import os
import google.auth
import googleapiclient.discovery
import googleapiclient.http
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

def create_sample_video(output_filename):
    """صناعة الفيديو التجريبي"""
    print("🎬 جاري إنشاء الفيديو...")
    try:
        # خلفية خضراء بمقاس Shorts
        bg = ColorClip(size=(1080, 1920), color=(0, 128, 0), duration=5)
        txt = TextClip("BuzzShorts AI Live", fontsize=80, color='white', font='Arial')
        txt = txt.set_position('center').set_duration(5)
        
        video = CompositeVideoClip([bg, txt])
        video.write_videofile(output_filename, fps=24, codec="libx264")
        print(f"✅ تم إنشاء: {output_filename}")
    except Exception as e:
        print(f"❌ فشل إنشاء الفيديو: {e}")

def get_youtube_client():
    """الاتصال بيوتيوب تلقائياً"""
    print("🔐 جاري المصادقة...")
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    # التقاط الهوية من نظام GitHub الجديد تلقائياً
    credentials, project = google.auth.default(scopes=scopes)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(youtube, file_path):
    """رفع الفيديو النهائي"""
    print(f"🚀 جاري الرفع إلى يوتيوب...")
    request_body = {
        "snippet": {
            "title": "BuzzShorts Automated Upload",
            "description": "تم الرفع بنجاح باستخدام Workload Identity!",
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)
    
    response = request.execute()
    print(f"🎊 مبروك! الفيديو الآن متاح هنا: https://youtu.be/{response['id']}")

if __name__ == "__main__":
    FILE = "final_short.mp4"
    create_sample_video(FILE)
    
    if os.path.exists(FILE):
        try:
            yt_client = get_youtube_client()
            upload_video(yt_client, FILE)
        except Exception as e:
            print(f"❌ خطأ أثناء الرفع: {e}")
            
