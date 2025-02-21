#!/bin/bash

# Start the rtsp-simple-server in the background
./rtsp-simple-server &

# Wait for a moment to ensure the server starts
sleep 2

# Execute the ffmpeg command
ffmpeg -f v4l2 -framerate 90 -re -stream_loop -1 -video_size 640x320 -input_format mjpeg -i /dev/video0 -c copy -f rtsp rtsp://localhost:8554/mystream
