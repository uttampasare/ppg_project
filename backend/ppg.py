import cv2
import numpy as np
import mediapipe as mp
from scipy.signal import butter, filtfilt

# -----------------------------
# Initialize MediaPipe FaceMesh
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
#     max_num_faces=1,
#     refine_landmarks=True,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------------
# Forehead ROI extraction
# -----------------------------
def get_face_roi(frame):
    if frame is None:
        print("Empty frame")
        return None

#     print("Frame shape:", frame.shape)
#     print("Frame dtype:", frame.dtype)
#     print("Frame min/max:", frame.min(), frame.max())
    frame = frame.astype(np.uint8)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_face_mesh.process(rgb)
#     print(frame.shape)
#     print(results)

    if not results.multi_face_landmarks:
        print("No face detected")
        return None

    if results.multi_face_landmarks:
        print("Face detected")

    landmarks = results.multi_face_landmarks[0]
    h, w, _ = frame.shape

    # Forehead landmarks (10 and 338)
    x1 = int(landmarks.landmark[10].x * w)
    y1 = int(landmarks.landmark[10].y * h)

    x2 = int(landmarks.landmark[338].x * w)
    y2 = int(landmarks.landmark[338].y * h)

    # Expand ROI
    x_min = max(0, min(x1, x2) - 20)
    x_max = min(w, max(x1, x2) + 20)
    y_min = max(0, min(y1, y2) - 40)
    y_max = min(h, max(y1, y2) + 20)

    roi = frame[y_min:y_max, x_min:x_max]

    if roi.size == 0:
        print("Empty ROI")
        return None

    return roi

# -----------------------------
# Bandpass filter (0.7–4 Hz)
# -----------------------------
def bandpass_filter(signal, fps):
    low = 0.7 / (fps / 2)
    high = 4.0 / (fps / 2)
    b, a = butter(3, [low, high], btype='band')
    return filtfilt(b, a, signal)

# -----------------------------
# Main PPG extraction function
# -----------------------------
def extract_ppg_from_video(path):
    print("Opening video:", path)
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print("Could not open video")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30  # fallback

    ppg_signal = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Downscale to reduce memory usage
        frame = cv2.resize(frame, (640, 480))

        roi = get_face_roi(frame)
        if roi is None:
            continue

        # Extract green channel mean
        green = np.mean(roi[:, :, 1])
        ppg_signal.append(green)

    cap.release()

    # -----------------------------
    # Validate signal
    # -----------------------------
    if len(ppg_signal) < 60:
        print("Not enough PPG data")
        return None

    ppg_signal = np.array(ppg_signal)

    # -----------------------------
    # Filter signal
    # -----------------------------
    filtered = bandpass_filter(ppg_signal, fps)

    # -----------------------------
    # FFT to find heart rate
    # -----------------------------
    freqs = np.fft.rfftfreq(len(filtered), d=1.0 / fps)
    fft_vals = np.abs(np.fft.rfft(filtered))

    # Limit to human heart rate range (40–180 BPM)
    valid = (freqs >= 0.7) & (freqs <= 3.0)
    freqs = freqs[valid]
    fft_vals = fft_vals[valid]

    if len(freqs) == 0:
        print("No valid frequency components")
        return None

    peak_freq = freqs[np.argmax(fft_vals)]
    bpm = int(peak_freq * 60)

    print("Estimated BPM:", bpm)
    return bpm