SentinelAI-Smart-Human-Detection-Alert-System

Overview

HumanGuard is an AI-powered security system that uses the YOLOv8 object detection model to identify human presence in real-time via a webcam. Upon detecting a person, the system triggers an alert sound, announces detection using text-to-speech (TTS), and sends an email notification to a predefined recipient. 

Features

Real-time Human Detection: Uses the YOLOv8 model for detecting humans from a webcam feed.
Audio Alert: Plays a buzzer sound upon detection.
Text-to-Speech Alert: Announces "Person detected" using Google TTS.
Email Notification: Sends an alert email when a person is detected.
Live Webcam Feed: Displays detection results with bounding boxes.
Prevents Repeated Alerts: Ensures notifications are sent only once per detection event.

Technologies Used

- Python
- OpenCV
- YOLOv8 (Ultralytics)
- Google Text-to-Speech (gTTS)
- SMTP (for email alerts)




