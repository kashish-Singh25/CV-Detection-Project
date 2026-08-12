import cv2
from ultralytics import YOLO
import pyttsx3
import threading

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Function to speak asynchronously
def speak(text):
    threading.Thread(target=lambda: engine.say(text) or engine.runAndWait()).start()

# Load YOLO model
model = YOLO('yolov8n.pt')

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform detection
    results = model(frame)

    # Draw detections on frame
    annotated_frame = results[0].plot()

    # Speak detected objects
    names_spoken = []
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        obj_name = model.names[cls_id]
        names_spoken.append(obj_name)

    if names_spoken:
        text_to_speak = ", ".join(set(names_spoken))
        speak(text_to_speak)

    # Show video
    cv2.imshow("Object Detection for Visually Impaired", annotated_frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
