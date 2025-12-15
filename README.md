User–Display Latency Measurement Tool

This repository provides a simple and practical way to measure user-to-display latency by analyzing a recorded screen session frame-by-frame.

The approach is based on detecting the time (in frames and milliseconds) between a user click and the corresponding visual change on the screen.

How It Works

You open a device (physical or mirrored) and navigate to a dedicated test webpage designed to make screen changes easy to detect.

You record your desktop screen while interacting with the webpage.

You provide the recorded video to the analysis program (latency.py).

The program automatically:

Detects click events

Detects visual changes on the screen

Counts the number of frames between each click and the corresponding screen update

Prints latency results in frames and milliseconds

Repository Contents

This repository includes:

Test Webpage
A public webpage used for latency testing:
👉 https://yossidar.github.io/latency-test

Latency Analysis Program

latency.py — analyzes a recorded video and measures latency

Example Recording

example.mp4 — sample desktop recording demonstrating the workflow

How to Use
1️⃣ Prerequisites

Install Python

Install required libraries:

pip install opencv-python numpy

2️⃣ Perform a Test Recording

Open your device or device mirror on your desktop.

Navigate to:
👉 https://yossidar.github.io/latency-test/

Start recording your desktop screen.

Click several times on the toggle button (the lower square).

On each click, the upper square toggles between black and white.

Stop the recording and save it as a video file.

3️⃣ Analyze the Recording

Download latency.py.

Place the recorded video file in the same folder as latency.py (for simplicity).

Run the analysis:

python latency.py record.mp4

4️⃣ Expected Output

You should see output similar to the following:

========================
Video FPS: 60.00

Latency results:
Frames (avg=51.25): [51, 50, 66, 48, 48, 44, 52, 51]
Millis (avg=854): [850, 833, 1100, 800, 800, 733, 867, 850]

Detected clicks: 8
========================


Frames: Number of frames between each click and the screen update

Millis: Latency in milliseconds (calculated from video FPS)

Detected clicks: Number of valid click events found in the recording

Debug Mode (Optional)

For validation and troubleshooting, you can run the program in debug mode:

python latency.py record.mp4 --debug


Debug mode will:

Save screenshots to a timestamped folder

Include:

Detected button area

Detected toggling square

Each click frame

Each corresponding screen-change frame

This allows visual verification that detection is working correctly.

Notes

The measurement is frame-accurate and independent of browser or OS timing.

Results depend on the FPS of the recording — higher FPS yields more precise measurements.

The tool is suitable for comparing latency across devices, environments, or configurations.
