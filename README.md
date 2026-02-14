# CVVideoPlayerLite

A lightweight [OpenCV](https://opencv.org/) video player designed to facilitate frame analysis.
It features real-time on-screen data including timestamp, frame index, and playback performance.

```python
import cv2 as cv

from video_player import VideoPlayer, HSize

player = VideoPlayer('../videos/5911716-hd_1920_1080_25fps.mp4')
player.resize(LSize.SD)
player.run()
```

![Man in Denim Jacket Riding His Fixie Bicycle Passing By](videos/5911716-hd_1920_1080_25fps.gif)

## Features

1. Resize OpenCV windows to SD, HD, or FHD resolutions (landscape or portrait).
Example: `player.resize(LSize.SD)`.
2. Callback support to handle external routines.
Example: `player.run(lambda image: cv.cvtColor(image, cv.COLOR_BGR2GRAY))`.
3. Start video playback from a specific timestamp.
Example: `player.run(start=1000)`.

## Controls

- SPACE: play or pause the video.
- ⬅️/➡️: step one frame backward or forward.
- ⬇️/⬆️: jump to first or last frame.

## Credits

- Video by cottonbro studio from Pexels:
https://www.pexels.com/video/man-in-denim-jacket-riding-his-fixie-bicycle-passing-by-5911716/.
It's free to use.
