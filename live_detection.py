import threading
import subprocess
import os
from detect import run_yolo_detection
import cv2

is_detecting = False
current_frame = None
latest_detection = None

def speak_message(text, enabled=True):
    if not enabled:
        return
    try:
        if os.name == "nt":
            subprocess.Popen(["powershell", "-Command", f'Start-SpeechSynthesizer \"{text}\"'])
        else:
            subprocess.Popen(["say", text])
    except Exception:
        pass

def start_detection(callback, voice_enabled=True):
    global is_detecting, current_frame, latest_detection
    is_detecting = True

    def detect_loop():
        global current_frame, latest_detection
        for frame, detections in run_yolo_detection():
            if not is_detecting:
                break
            if detections:
                latest_detection = detections[-1]
                speak_message(f"{detections[-1][0]} detected", voice_enabled)
            current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            callback(current_frame, latest_detection)

    thread = threading.Thread(target=detect_loop, daemon=True)
    thread.start()

def stop_detection():
    global is_detecting
    is_detecting = False
