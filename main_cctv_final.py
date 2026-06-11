import cv2
import time
from supabase import create_client
import requests

# --- CONFIGURATION ---
SUPABASE_URL = "https://xfgjjluogifdmgpabbgk.supabase.co"
SUPABASE_KEY = "sb_publishable_B6b9PHhWpmFMpnIS800t2g_kYw0B-aa"
TELEGRAM_TOKEN = "8085719035:AAEJEcOV8ryEJgPU5EY34OeaoW2BbuvL9II"
CHAT_ID = "8522771910"
CAMERA_URL = "http://10.204.144.135:8080:8080/video" # Apna IP Webcam URL daalein

# Initialize Clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
cap = cv2.VideoCapture(CAMERA_URL)

def send_alerts(file_path):
    # 1. Telegram Alert
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(file_path, 'rb') as photo:
        requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': photo})
    
    # 2. Supabase Cloud Upload
    file_name = f"alert_{int(time.time())}.jpg"
    with open(file_path, 'rb') as f:
        supabase.storage.from_("cctv-alerts").upload(path=file_name, file=f)
    print(f"Alert Sent! Saved as {file_name}")

# --- MAIN LOOP ---
while True:
    ret, frame = cap.read()
    if not ret: break
    
    # Yahan aapka motion detection logic aayega (frame differencing)
    # Agar motion detect hua:
    # cv2.imwrite("current_alert.jpg", frame)
    # send_alerts("current_alert.jpg")
    
    cv2.imshow("Smart CCTV Live", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()