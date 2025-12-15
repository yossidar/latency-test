The purpose of the repo is to help with measuring user-display latency.

**How it works:**
---------------
1. You open a device and navigate to a dedicated webpage that simplifies screen change detection.
2. You record your desktop screen and perform several clicks on this webpage.
3. You provide the recording to the program (latency.py), which counts the frames between each click and the corresponding change on the screen and prints the results.


**This repo contains:**
---------------------
1. The webpage (public and published: https://yossidar.github.io/latency-test)
2. The latency test program: latency.py
3. An example of a recorded desktop session: example.mp4


**How to use:**
-------------
1. Install Python.
2. Install required libraries: pip install opencv-python numpy
3. Open a device and navigate to: https://yossidar.github.io/latency-test/
4. Start recording your screen.
5. Click several times on the toggle button (the lower square) – the upper square should toggle colors between black and white on each click.
6. Save the recording to a file.
7. Download latency.py.
8. Put the recorded video in the same folder (for simplicity).
9. Run: python .\latency.py .\record.mp4
   You should expect output similar to this:
```
========================
Video FPS: 60.00

Latency results:
Frames (avg=51.25): [51, 50, 66, 48, 48, 44, 52, 51]
Millis (avg=854): [850, 833, 1100, 800, 800, 733, 867, 850]

Detected clicks: 8
========================
```
11. Debug mode: You can run it in debug mode:
Run: python .\latency.py .\record.mp4 --debug
It will save screenshots into a folder showing the detected button area, the toggled square, and each click/color change.
