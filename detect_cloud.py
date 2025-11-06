import os
import pandas as pd
from datetime import datetime

logs_file = "logs.csv"

def run_yolo_detection():
    print("🌐 Cloud Mode: YOLO detection disabled (OpenCV not supported).")
    # This just yields nothing, to keep app structure intact
    yield None, []

def is_cloud_environment():
    return os.environ.get("STREAMLIT_RUNTIME") == "true"
