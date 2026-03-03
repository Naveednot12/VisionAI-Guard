# VisionAI Guard

Real-time object detection dashboard powered by **YOLOv8** and **Streamlit**. Detects objects through your webcam, draws bounding boxes on a live preview, and logs detections to a CSV file.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![YOLOv8](https://img.shields.io/badge/YOLOv8-ultralytics-green)

---

## Features

- **Live Camera Detection** — Real-time YOLOv8 object detection with bounding boxes displayed in the browser.
- **Dashboard** — View detection logs with timestamps and confidence scores.
- **Smart Logging** — Each object class is logged once every 30 seconds to avoid duplicate entries. Low-confidence detections (below 50%) are filtered out.
- **Cloud-Safe** — Gracefully falls back to a placeholder UI when deployed on Streamlit Cloud (no camera access).

---

## Project Structure

```
VisionAIGuard/
├── app.py               # Streamlit UI (dashboard + live detection)
├── detect.py            # YOLOv8 local detection with logging
├── detect_cloud.py      # Cloud fallback (no-op detection)
├── live_detection.py    # Threaded camera loop
├── yolov8n.pt           # YOLOv8 nano model weights
├── requirements.txt     # Python dependencies
├── logs.csv             # Detection logs (auto-generated)
└── .gitignore
```

---

## How to Run

### Prerequisites

- **Python 3.10+** installed
- A **webcam** connected to your device

### 1. Clone the repository

```bash
git clone https://github.com/Naveednot12/VisionAI-Guard.git
cd VisionAI-Guard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at **http://localhost:8501**.

### 4. Start detecting

1. Select **🎥 Live Detection** from the sidebar.
2. Click **🟢 Start Detection** to begin.
3. Objects detected by your webcam will appear with bounding boxes in the live preview.
4. Switch to **📊 Dashboard** to view the detection logs.

---

## Configuration

You can tweak detection settings in `detect.py`:

| Setting | Default | Description |
|---|---|---|
| `COOLDOWN_SECONDS` | `30` | Seconds before the same object class is logged again |
| `MIN_CONFIDENCE` | `0.50` | Minimum confidence threshold — detections below this are ignored |
| `imgsz` | `320` | YOLO input image size — smaller = faster, larger = more accurate |

---

## Notes

- **Streamlit Cloud** does not support webcam access. The app will show a placeholder UI in cloud mode. For full functionality, run locally.
- Detection logs are saved to `logs.csv` in the project root.
- The YOLOv8 nano model (`yolov8n.pt`) is used for fast inference. You can swap it for a larger model (e.g., `yolov8s.pt`, `yolov8m.pt`) for better accuracy at the cost of speed.

---

## License

This project is open source and available for personal and educational use.
