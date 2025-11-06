import os
import pandas as pd
import numpy as np

# 🧠 Try importing OpenCV safely
try:
    import cv2
except ImportError:
    cv2 = None
    print("⚠️ OpenCV not available in this environment. Running in Cloud-Safe Mode.")

from ultralytics import YOLO
from datetime import datetime

# 🧠 Load YOLO model only if cv2 is available
model = YOLO("yolov8n.pt") if cv2 else None
logs_file = "logs.csv"


def run_yolo_detection():
    """
    Runs YOLOv8 detection locally.
    On Streamlit Cloud (no cv2), it runs in safe mode (skips detection).
    """

    # 🌐 Skip detection if OpenCV is missing (Cloud mode)
    if cv2 is None:
        print("⚠️ YOLO detection skipped (cv2 not available in cloud).")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot access camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, stream=True)
        detections = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                name = model.names[cls]
                detections.append((name, conf))

                # 🟢 Draw boxes
                xyxy = box.xyxy[0].cpu().numpy().astype(int)
                cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} {conf:.2f}", (xyxy[0], xyxy[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 🗂️ Log detections
        if detections:
            df = pd.DataFrame(detections, columns=["object", "confidence"])
            df["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df.to_csv(logs_file, mode="a", header=not os.path.exists(logs_file), index=False)

        yield frame, detections

    cap.release()
    cv2.destroyAllWindows()
