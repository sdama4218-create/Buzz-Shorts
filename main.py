import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# 1. جلب البيانات من GitHub Secrets (التي عرفناها في ملف YAML)
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('GOOGLE_REFRESH_TOKEN')
API_KEY = os.environ.get('GOOGLE_API_KEY')

def get_youtube_client():
    """إنشاء اتصال مع يوتيوب باستخدام الـ Refresh Token"""
    creds = Credentials(
        token=None,  # سيتم تحديثه تلقائياً
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    
    # تجديد الـ Access Token إذا انتهى
    if not creds.valid:
        creds.refresh(Request())
        
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def upload_video(youtube, file_path, title, description):
    """دالة رفع الفيديو"""
    request_body = {
        "snippet": {
            "categoryId": "22",  # تصنيف People & Blogs
            "title": title,
            "description": description,
            "tags": ["AI", "Shorts", "Automation"]
        },
        "status": {
            "privacyStatus": "public",  # أو "private" للتجربة
            "selfDeclaredMadeForKids": False
        }
    }
    
    # إعداد عملية الرفع
    media_file = googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )
    
    print(f"جاري رفع الفيديو: {title}...")
    response = request.execute()
    print(f"تم الرفع بنجاح! رابط الفيديو: https://youtu.be/{response['id']}")

if __name__ == "__main__":
    # ملاحظة: تأكد أن ملف الفيديو موجود في مشروعك بنفس الاسم
    VIDEO_FILE = "output_video.mp4" 
    
    if os.path.exists(VIDEO_FILE):
        try:
            youtube_client = get_youtube_client()
            upload_video(
                youtube_client, 
                VIDEO_FILE, 
                "فيديو رهيب تم إنشاؤه بالذكاء الاصطناعي", 
                "هذا الفيديو تم رفعه تلقائياً بواسطة بوت BuzzShorts"
            )
        except Exception as e:
            print(f"حدث خطأ أثناء الرفع: {e}")
    else:
        print(f"خطأ: لم يتم العثور على ملف {VIDEO_FILE}. تأكد من أن كود إنشاء الفيديو يعمل أولاً.")
        
