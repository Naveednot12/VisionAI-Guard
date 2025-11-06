import os
import pandas as pd
from datetime import datetime
import time

logs_file = "logs.csv"

def run_yolo_detection():
    print("🌐 Cloud Mode: YOLO disabled — no camera available.")
    while True:
        time.sleep(1)
        yield None, []

def is_cloud_environment():
    return os.environ.get("STREAMLIT_RUNTIME") == "true"
