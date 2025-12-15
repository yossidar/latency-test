The purpose of the repo is to help with misurring user-display latency.

How it works:
1. You open a device and nevigate to a dedicated webpage that simplifies screen changes detection.
2. You record your desktop screen and perform some clicks in this webpage.
3. You give the record to the program (latency.py) that counts the frames frames between each click to the change on the screen and print the results.

This repo contains:
1. The webpage (public and published. https://yossidar.github.io/latency-test)
2. The latency-test program: latency.py
3. Example of a recorded desktop session: example.mp4

How to use:
1. Install python
2. Install required libraries: pip install opencv-python numpy
3. Open device >> navigate to >> https://yossidar.github.io/latency-test/
4. Start record your screen
5. Click several times on the toggle button (the lower square) - the upper square should toggle colors between black and white on each click.
6. Save your record to a file.
7. Download latency.py
8. Put the record video at the same folder (just for simplicity)
9. Run:  python .\latency.py .\record.mp4
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
   It will save into a folder screenshot of the detected area of the Button, the toggled square, and each click/color-change.
         
