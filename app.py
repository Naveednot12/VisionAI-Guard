import streamlit as st
import pandas as pd
from live_detection import start_detection, stop_detection, current_frame, latest_detection
from assistant import query_assistant
import os
import time

logs_file = "logs.csv"

st.set_page_config(page_title="VisionAI Guard", layout="wide", page_icon="🧠")

st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🎥 Live Detection", "💬 AI Assistant"])

# Shared state
if "voice_enabled" not in st.session_state:
    st.session_state["voice_enabled"] = True
if "detection_running" not in st.session_state:
    st.session_state["detection_running"] = False

# ---------------- DASHBOARD ----------------
if page == "📊 Dashboard":
    st.title("🧠 VisionAI Guard Dashboard")
    st.write("Monitor real-time detections and analyze insights with AI assistance.")

    st.subheader("📊 Detection Logs")
    if os.path.exists(logs_file):
        df = pd.read_csv(logs_file)
        st.dataframe(df.tail(300), use_container_width=True)
    else:
        st.warning("No detection logs yet. Start detection to generate logs.")


# ---------------- LIVE DETECTION ----------------
elif page == "🎥 Live Detection":
    st.title("🎥 Real-Time Detection")
    st.write("Start your camera to run YOLO detection in real time.")

    # --- Side-by-side layout (Control panel + Live Preview) ---
    col1, col2 = st.columns([1.2, 2.5])

    # LEFT: Controls + Status
    with col1:
        st.subheader("🎛️ Control Panel")

        start_btn = st.button("🟢 Start Detection", use_container_width=True)
        stop_btn = st.button("🔴 Stop Detection", use_container_width=True)
        st.session_state["voice_enabled"] = st.checkbox(
            "🔊 Voice Alerts", value=st.session_state["voice_enabled"]
        )

        st.subheader("📡 Live Status")
        if latest_detection:
            st.success(f"Detected: {latest_detection[0]} | Confidence: {latest_detection[1]:.2f}")
        elif st.session_state["detection_running"]:
            st.info("Detecting objects...")
        else:
            st.warning("No detections yet.")

    # RIGHT: Live Camera Preview
    with col2:
        st.subheader("🎦 Live Camera Preview")
        preview_placeholder = st.empty()

        # Start detection
        if start_btn:
            start_detection(lambda f, d: None, voice_enabled=st.session_state["voice_enabled"])
            st.session_state["detection_running"] = True
            st.success("🟢 Detection started...")

        # Stop detection
        if stop_btn:
            stop_detection()
            st.session_state["detection_running"] = False
            preview_placeholder.empty()  # 🔧 clear the preview box instantly
            st.warning("🛑 Detection stopped.")
            time.sleep(0.5)  # 🔧 small delay to let Streamlit update before rerun

        # Continuous refresh for live preview
        if st.session_state["detection_running"]:
            while st.session_state["detection_running"]:
                if current_frame is not None:
                    preview_placeholder.image(current_frame, channels="RGB", use_container_width=True)
                time.sleep(0.1)
                st.rerun()
        else:
            # show info only if no preview
            st.info("Start detection to see live preview here.")


# ---------------- AI ASSISTANT ----------------
elif page == "💬 AI Assistant":
    st.title("💬 VisionAI Assistant")
    st.write("Ask your assistant about today's detections.")

    if os.path.exists(logs_file):
        st.dataframe(pd.read_csv(logs_file).tail(10), use_container_width=True)

    query = st.text_input("Ask a question:", placeholder="e.g., How many persons were detected today?")
    if query:
        st.write(query_assistant(query))
