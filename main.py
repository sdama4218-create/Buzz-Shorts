import os
import google.auth
import googleapiclient.discovery
import googleapiclient.http

def get_youtube_client():
    """الاتصال بيوتيوب باستخدام الهوية التلقائية"""
    print("🔐 جاري المصادقة...")
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    # التقاط الهوية من نظام GitHub الجديد تلقائياً
    credentials, project = google.auth.default(scopes=scopes)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(youtube, file_path):
    """رفع الفيديو الجاهز"""
    if not os.path.exists(file_path):
        print(f"❌ خطأ: لم يتم العثور على الملف {file_path}")
        return

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
    # اسم الفيديو الذي يجب أن يكون موجوداً في مستودعك
    FILE = "my_video.mp4" 
    
    try:
        yt_client = get_youtube_client()
        upload_video(yt_client, FILE)
    except Exception as e:
        print(f"❌ خطأ أثناء الرفع: {e}")
        
