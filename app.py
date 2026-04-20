import streamlit as st
import cv2
import tempfile
from ultralytics import YOLO
import os

# Title
st.title("🐔 Poultry Dullness Detection (YOLOv8)")
st.write("Upload a video and detect dullness automatically")

# Load model (cache to avoid reloading every time)
@st.cache_resource
def load_model():
    return YOLO(r"D:\dullnessdetect\runs\detect\chicken_health_model\weights\best.pt")

model = load_model()

# Upload video
uploaded_file = st.file_uploader("📤 Upload Video", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    st.video(uploaded_file)

    # Save uploaded video to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    input_path = tfile.name
    output_path = os.path.join(tempfile.gettempdir(), "output.mp4")

    if st.button("▶️ Run Detection"):
        st.info("Processing video... please wait ⏳")

        cap = cv2.VideoCapture(input_path)

        width = int(cap.get(3))
        height = int(cap.get(4))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        progress = st.progress(0)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # YOLO prediction
            results = model.predict(frame, conf=0.3)
            annotated_frame = results[0].plot()

            out.write(annotated_frame)

            # Update progress
            current_frame += 1
            progress.progress(min(current_frame / frame_count, 1.0))

        cap.release()
        out.release()

        st.success("Processing completed!")

        # Show output video
        st.video(output_path)

        # Download button
        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Download Output Video",
                data=f,
                file_name="processed_video.mp4",
                mime="video/mp4"
            )