import cv2
import requests
import numpy as np
import time

# --- APNI DETAILS YAHAN DALO ---
TOKEN = "8085719035:AAEJEcOV8ryEJgPU5EY34OeaoW2BbuvL9II" # Apna pura token dalo
CHAT_ID = "8522771910"
URL = "http://10.204.144.135:8080/shot.jpg" # Shot.jpg fast chalta hai
# ------------------------------

def send_telegram_photo(frame):
    photo_path = "alert.jpg"
    cv2.imwrite(photo_path, frame) # Photo save ki
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    files = {'photo': open(photo_path, 'rb')}
    data = {'chat_id': CHAT_ID, 'caption': "⚠️ ALERT: Motion Detected! Koi aaya hai."}
    
    try:
        requests.post(url, files=files, data=data)
        print("Telegram alert sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Pehla frame lene ke liye
img_resp = requests.get(URL)
img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
frame1 = cv2.imdecode(img_arr, -1)

last_alert_time = 0

print("CCTV System Active... Press 'q' to stop.")

while True:
    # Naya frame lena
    img_resp = requests.get(URL)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame2 = cv2.imdecode(img_arr, -1)

    # Motion detection logic
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 10000: # Sensitivity handle karne ke liye
            continue
        
        # Agar motion bada hai, toh alert bhejo
        current_time = time.time()
        if current_time - last_alert_time > 15: # 15 sec ka gap taaki spam na ho
            print("Motion Detected! Sending Photo...")
            send_telegram_photo(frame2)
            last_alert_time = current_time

    cv2.imshow("Smart CCTV Feed", frame2)
    frame1 = frame2 # Update frame

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()