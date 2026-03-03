import streamlit as st
import pandas as pd
import os
import time

# ---------------- ENVIRONMENT DETECTION ----------------
is_cloud = os.environ.get("STREAMLIT_RUNTIME") == "true" or os.environ.get("HOME", "").startswith("/mount")

logs_file = "logs.csv"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="VisionAI Guard", layout="wide", page_icon="🧠")

st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🎥 Live Detection"])

# ---------------- SESSION STATE ----------------
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
        st.dataframe(df.tail(300), width='stretch')
    else:
        st.warning("No detection logs yet. Start detection to generate logs.")

# ---------------- LIVE DETECTION ----------------
elif page == "🎥 Live Detection":
    st.title("🎥 Real-Time Detection")

    # 🚨 Important note about Streamlit Cloud
    st.info(
        "⚠️ **Note:** OpenCV-based live camera detection will not work on Streamlit Cloud "
        "because it does not allow direct webcam or local device access.\n\n"
        "👉 To use real-time detection, please run this app locally using the command:\n"
        "`streamlit run app.py`"
    )

    if is_cloud:
        # CLOUD MODE UI
        st.markdown(
            """
            <div style='
                background-color:#1e1e1e;
                border:2px solid #444;
                border-radius:15px;
                padding:60px 30px;
                text-align:center;
                color:white;
                box-shadow:0 0 20px rgba(0,0,0,0.3);
            '>
            <h2>🌐 Cloud Mode Active</h2>
            <p style='font-size:18px;'>Live camera access is not available on Streamlit Cloud.</p>
            <p style='color:#aaa;'>To use real-time detection, run this app locally.</p>
            </div>
            <br>
            <div style='
                background-color:#111;
                border:2px dashed #555;
                border-radius:10px;
                padding:80px 30px;
                text-align:center;
                color:#666;
            '>
            <h1>📷</h1>
            <h3>Camera Preview Unavailable</h3>
            <p>Connect a webcam and run locally to see the live feed here.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        # 🖥️ LOCAL MODE (Camera available)
        import live_detection

        # Create two main columns (left = controls, right = preview)
        col1, col2 = st.columns([1, 2])

        # LEFT SIDE → Controls and Live Status
        with col1:
            st.subheader("🎮 Controls")
            start_btn = st.button("🟢 Start Detection", use_container_width=True)
            stop_btn = st.button("🔴 Stop Detection", use_container_width=True)
            st.session_state["voice_enabled"] = st.checkbox(
                "🔊 Voice Alerts", value=st.session_state["voice_enabled"]
            )

            st.subheader("📡 Live Status")
            if live_detection.latest_detection:
                st.success(f"Detected: {live_detection.latest_detection[0]} | Confidence: {live_detection.latest_detection[1]:.2f}")
            elif st.session_state["detection_running"]:
                st.info("Detecting objects...")
            else:
                st.warning("No detections yet.")

        # RIGHT SIDE → Live Camera Preview
        with col2:
            st.subheader("🎦 Live Camera Preview")
            preview_placeholder = st.empty()

            # Start detection
            if start_btn:
                live_detection.start_detection(lambda f, d: None, voice_enabled=st.session_state["voice_enabled"])
                st.session_state["detection_running"] = True
                st.success("🟢 Detection started...")

            # Stop detection
            if stop_btn:
                live_detection.stop_detection()
                st.session_state["detection_running"] = False
                preview_placeholder.empty()  # ✅ Immediately clear preview
                st.warning("🛑 Detection stopped.")

            # Continuous refresh for live preview
            if st.session_state["detection_running"]:
                if live_detection.current_frame is not None:
                    preview_placeholder.image(
                        live_detection.current_frame, channels="RGB", width="stretch"
                    )
                time.sleep(0.15)
                st.rerun()
            else:
                # ✅ Don’t show the last frame after stop
                preview_placeholder.empty()
                st.info("Start detection to see live preview here.")
