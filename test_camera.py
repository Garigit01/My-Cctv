import cv2

# Yahan apna IP Webcam wala address daalein
# Example: "http://192.168.1.5:8080/video"
url = "http://10.204.144.135:8080/video" 

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera nahi mil raha, check connection!")
        break
    
    cv2.imshow('CCTV Live Feed', frame)

    # 'q' dabane se window band ho jayegi
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()