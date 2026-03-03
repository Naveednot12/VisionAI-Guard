import os
import threading

current_frame = None
latest_detection = None
detection_thread = None
running = False

# Detect if the app runs on Streamlit Cloud
is_cloud = os.environ.get("STREAMLIT_RUNTIME") == "true"

# Safe import logic
if is_cloud:
    print("Running on Streamlit Cloud - loading cloud-safe detection.")
    from detect_cloud import run_yolo_detection
else:
    try:
        from detect import run_yolo_detection
    except Exception as e:
        print("Local YOLO import failed, using safe fallback:", e)
        from detect_cloud import run_yolo_detection


def detect_loop(callback=None):
    global current_frame, latest_detection, running

    for frame, detections in run_yolo_detection():
        if not running:
            break

        if frame is not None:
            current_frame = frame
        if detections:
            latest_detection = detections[0]

        if callback:
            callback(frame, detections)

    running = False


def start_detection(callback=None, voice_enabled=False):
    global running, detection_thread

    if running:
        print("Detection is already running.")
        return

    running = True
    detection_thread = threading.Thread(target=detect_loop, args=(callback,), daemon=True)
    detection_thread.start()
    print("Detection started.")


def stop_detection():
    global running, current_frame, latest_detection
    if running:
        running = False
        current_frame = None
        latest_detection = None
        print("Detection stopped.")
    else:
        print("Detection was not running.")
