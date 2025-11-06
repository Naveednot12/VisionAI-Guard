import cv2
from ultralytics import YOLO
import pandas as pd
import os
import time

logs_file = "logs.csv"

def run_yolo_detection(model_path="yolov8n.pt"):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access webcam.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        boxes = results[0].boxes

        detections = []
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]
            detections.append((label, conf))

            # ✅ Safe logging
            try:
                df = pd.DataFrame([[time.strftime("%Y-%m-%d %H:%M:%S"), label, conf]],
                                  columns=["time", "object", "confidence"])
                df.to_csv(logs_file, mode="a", header=not os.path.exists(logs_file), index=False)
            except PermissionError:
                print("⚠️ Warning: logs.csv is currently locked. Skipping write...")

        yield frame, detections

    cap.release()
