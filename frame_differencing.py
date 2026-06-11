import cv2

# Phone ka IP address yahan update karein
url = "http://10.204.144.135:8080/video" 
cap = cv2.VideoCapture(url)

# Pehla frame store karne ke liye
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    # Do frames ke beech ka antar (difference) nikalna
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 1000: # Choti halchal (makkhi etc.) ko ignore karega
            continue
        
        # Agar badi halchal hui toh rectangle banao
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "STATUS: MOTION DETECTED", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Smart CCTV Feed", frame1)
    
    # Frames ko update karna
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()