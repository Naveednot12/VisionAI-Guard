import os
import csv
import time
import numpy as np

# Try importing OpenCV safely
try:
    import cv2
except ImportError:
    cv2 = None
    print("⚠️ OpenCV not available in this environment. Running in Cloud-Safe Mode.")

from ultralytics import YOLO
from datetime import datetime

# Load YOLO model only if cv2 is available
model = YOLO("yolov8n.pt") if cv2 else None
logs_file = "logs.csv"

# Cooldown tracking: only log each object class once per COOLDOWN_SECONDS
COOLDOWN_SECONDS = 30
MIN_CONFIDENCE = 0.50  # Ignore detections below this confidence
_last_logged = {}  # {object_name: timestamp}


def _log_detections(detections):
    """Log only new/cooldown-expired detections to CSV efficiently."""
    now = time.time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_log = []

    for name, conf in detections:
        if conf < MIN_CONFIDENCE:
            continue
        last = _last_logged.get(name, 0)
        if now - last >= COOLDOWN_SECONDS:
            to_log.append((name, conf, timestamp))
            _last_logged[name] = now

    if not to_log:
        return

    file_exists = os.path.exists(logs_file)
    with open(logs_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["object", "confidence", "time"])
        for row in to_log:
            writer.writerow(row)


def run_yolo_detection():
    """
    Runs YOLOv8 detection locally using the webcam.
    Yields (frame, detections) for each captured frame.
    On Streamlit Cloud (no cv2), it skips detection.
    """
    if cv2 is None:
        print("⚠️ YOLO detection skipped (cv2 not available in cloud).")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot access camera.")
        return

    # Reduce camera resolution for faster processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO with smaller input size and verbose=False for speed
        results = model(frame, imgsz=320, verbose=False)
        detections = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls]
                detections.append((name, conf))

                # Draw bounding boxes
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} {conf:.2f}", (xyxy[0], xyxy[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Log detections with cooldown (avoids spamming logs)
        if detections:
            _log_detections(detections)

        # Convert BGR to RGB for Streamlit display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        yield frame_rgb, detections

    cap.release()
