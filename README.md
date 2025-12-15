User-Display Latency Measurement Tool

This repository provides a simple way to measure user-to-display latency by analyzing a recorded screen session frame by frame.

The tool measures the time between a user click and the corresponding visual change on the screen, reported in both frames and milliseconds.

How It Works

Open a device (physical or mirrored) and navigate to a dedicated test webpage that simplifies screen-change detection.

Record your desktop screen while interacting with the webpage.

Provide the recorded video to the analysis program (latency.py).

The program detects click events, detects screen updates, and counts the number of frames between each click and the corresponding visual change.

Repository Contents

This repository contains:

Test webpage (public and published):
https://yossidar.github.io/latency-test

Latency analysis program:
latency.py

Example recorded desktop session:
example.mp4

How to Use
Prerequisites

Install Python

Install required libraries:
pip install opencv-python numpy

Perform a Test Recording

Open your device or device mirror on your desktop.

Navigate to:
https://yossidar.github.io/latency-test/

Start recording your desktop screen.

Click several times on the toggle button (the lower square).
On each click, the upper square toggles between black and white.

Stop the recording and save it as a video file.

Analyze the Recording

Download latency.py.

Place the recorded video file in the same folder as latency.py (for simplicity).

Run:
python latency.py record.mp4

Example Output

========================
Video FPS: 60.00

Latency results:
Frames (avg=51.25): [51, 50, 66, 48, 48, 44, 52, 51]
Millis (avg=854): [850, 833, 1100, 800, 800, 733, 867, 850]

Detected clicks: 8

Frames: number of frames between each click and screen update
Millis: latency in milliseconds based on video FPS
Detected clicks: number of valid click events detected

Debug Mode

You can run the program in debug mode:

python latency.py record.mp4 --debug

In debug mode, the program saves screenshots to a timestamped folder, including:

Detected button area

Detected toggling square

Each click frame

Each corresponding screen-change frame

This allows visual validation that detection is working correctly.

Notes

Measurements are frame-accurate and independent of browser or OS timing.

Accuracy depends on the FPS of the recorded video.

Higher FPS recordings provide more precise latency measurements.
