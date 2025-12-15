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
    Video FPS: 60.00

    Latency results:
    Frames (avg=51.25): [51, 50, 66, 48, 48, 44, 52, 51]
    Millis (avg=854.17): [850.0, 833.33, 1100.0, 800.0, 800.0, 733.33, 866.67, 850.0]

    Detected clicks: 8
10. Debug mode: You can run it in debug mode:
   Run: python .\latency.py .\record.mp4 --debug
   It will save into a folder screenshot of the detected area of the Button, the toggled square, and each click/color-change.
         
