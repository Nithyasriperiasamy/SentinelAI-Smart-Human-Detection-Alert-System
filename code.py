import cv2
import time
import os
from ultralytics import YOLO
from gtts import gTTS
from playsound import playsound
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # You can use 'yolov8s.pt' or other versions

# Initialize webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam

# Email settings
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_password"  # Use an app password if using Gmail
RECIPIENT_EMAIL = "recipient_email@gmail.com"

def send_email():
    """Send an email alert when a person is detected."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = "Alert: Person Detected!"

    body = "A person has been detected by the YOLOv8 security system."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", str(e))

def play_alarm():
    """Play a pre-downloaded alarm sound."""
    alarm_file = "buzzer.mp3"  # Ensure this file exists in your working directory
    playsound(alarm_file)

def say_person_detected():
    """Use gTTS to generate and play 'Person detected' audio."""
    tts = gTTS(text="Person detected", lang='en')
    audio_file = "alert.mp3"
    tts.save(audio_file)
    playsound(audio_file)
    os.remove(audio_file)

person_detected = False  # Prevent multiple alerts for the same detection

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Perform object detection
    results = model(frame)

    # Draw bounding boxes and check if a person is detected
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            if class_id == 0:  # Class ID 0 corresponds to "person" in COCO dataset
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if not person_detected:
                    play_alarm()
                    say_person_detected()
                    send_email()
                    person_detected = True  # Avoid continuous alerts

    cv2.imshow("YOLOv8 Person Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
