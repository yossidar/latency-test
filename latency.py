import cv2
import numpy as np
import sys
import os
from datetime import datetime

# ==========================
# ARGUMENTS
# ==========================
if len(sys.argv) < 2:
    print("Usage: python latency.py <video_file> [--debug]")
    sys.exit(1)

VIDEO_PATH = sys.argv[1]
DEBUG = "--debug" in sys.argv

if not os.path.isfile(VIDEO_PATH):
    print(f"Error: file not found: {VIDEO_PATH}")
    sys.exit(1)

# ==========================
# DEBUG OUTPUT FOLDER
# ==========================
DEBUG_DIR = None
if DEBUG:
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    DEBUG_DIR = f"screenshots_{ts}"
    os.makedirs(DEBUG_DIR, exist_ok=True)

# ==========================
# THRESHOLDS
# ==========================
BRIGHTNESS_DELTA = 40
RED_PIXELS_ON = 25
RED_PIXELS_OFF = 10

# ==========================
# HELPERS
# ==========================
def clamp_roi(x, y, w, h, W, H):
    x = max(0, min(x, W - 1))
    y = max(0, min(y, H - 1))
    w = max(1, min(w, W - x))
    h = max(1, min(h, H - y))
    return (x, y, w, h)

def find_square_roi(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best = None
    best_area = 0

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        aspect = w / float(h)

        if area > best_area and 0.8 < aspect < 1.2 and area > 200:
            best = (x, y, w, h)
            best_area = area

    return best

def square_brightness(frame, roi):
    x, y, w, h = roi
    gray = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray))

def red_pixel_count(frame, roi):
    x, y, w, h = roi
    sub = frame[y:y+h, x:x+w]
    hsv = cv2.cvtColor(sub, cv2.COLOR_BGR2HSV)

    lower1 = np.array([0, 120, 70])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 120, 70])
    upper2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)
    return int(cv2.countNonZero(mask))

def compute_button_roi_from_square(square_roi, frame_shape):
    H, W = frame_shape[:2]
    sx, sy, sw, sh = square_roi

    bw = int(sw * 0.9)
    bh = int(sh * 0.9)

    bx = int(sx + sw / 2 - bw / 2)
    by = int(sy + sh + sh * 0.15)

    return clamp_roi(bx, by, bw, bh, W, H)

# ==========================
# MAIN
# ==========================
cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)

ret, first_frame = cap.read()
if not ret:
    print("Error: cannot read video")
    sys.exit(1)

square_roi = find_square_roi(first_frame)
if square_roi is None:
    print("Error: square not detected automatically")
    sys.exit(1)

button_roi = compute_button_roi_from_square(square_roi, first_frame.shape)

print(f"Video FPS: {fps:.2f}")

if DEBUG:
    print(f"Detected SquareROI: {square_roi}")
    print(f"Detected ButtonROI: {button_roi}")

    sx, sy, sw, sh = square_roi
    bx, by, bw, bh = button_roi
    cv2.imwrite(os.path.join(DEBUG_DIR, "SquareROI.jpg"),
                first_frame[sy:sy+sh, sx:sx+sw])
    cv2.imwrite(os.path.join(DEBUG_DIR, "ButtonROI.jpg"),
                first_frame[by:by+bh, bx:bx+bw])

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

frame_idx = 0
click_index = 0
latencies_frames = []
latencies_ms = []

waiting_for_change = False
click_frame_idx = None
prev_brightness = None
prev_red_present = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    brightness = square_brightness(frame, square_roi)
    if prev_brightness is None:
        prev_brightness = brightness

    red_cnt = red_pixel_count(frame, button_roi)
    red_present = red_cnt >= RED_PIXELS_ON

    if red_present and not prev_red_present and not waiting_for_change:
        click_index += 1
        click_frame_idx = frame_idx
        waiting_for_change = True

        if DEBUG:
            cv2.imwrite(os.path.join(DEBUG_DIR, f"{click_index}click.jpg"), frame)

    if waiting_for_change and abs(brightness - prev_brightness) > BRIGHTNESS_DELTA:
        delta_frames = frame_idx - click_frame_idx
        latencies_frames.append(delta_frames)

        if fps and fps > 0:
            latencies_ms.append(round(delta_frames * 1000.0 / fps, 2))
        else:
            latencies_ms.append(None)

        waiting_for_change = False

        if DEBUG:
            cv2.imwrite(os.path.join(DEBUG_DIR, f"{click_index}change.jpg"), frame)

    prev_brightness = brightness
    prev_red_present = red_present if red_cnt >= RED_PIXELS_OFF else False
    frame_idx += 1

cap.release()

# ==========================
# RESULTS
# ==========================
avg_frames = round(sum(latencies_frames) / len(latencies_frames), 2) if latencies_frames else 0
avg_ms = round(sum(latencies_ms) / len(latencies_ms), 2) if latencies_ms else 0

print("\nLatency results:")
print(f"Frames (avg={avg_frames}): {latencies_frames}")
print(f"Millis (avg={avg_ms}): {latencies_ms}")

print(f"\nDetected clicks: {click_index}")

if DEBUG:
    print(f"\nScreenshots saved to folder: {DEBUG_DIR}")
