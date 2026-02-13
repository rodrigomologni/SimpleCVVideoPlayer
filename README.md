# SimpleCVVideoPlayer

A simple [OpenCV](https://opencv.org/) video player to help analyze video frames and learn about the library.
The player displays the frame time and index, and processing rate.

![Man in Denim Jacket Riding His Fixie Bicycle Passing By](videos/5911716-hd_1920_1080_25fps.gif)

## Example

```python
import cv2 as cv

from video_player import VideoPlayer, HSize

player = VideoPlayer('../videos/5911716-hd_1920_1080_25fps.mp4')
player.resize(HSize.SD)
player.run(lambda image: cv.cvtColor(image, cv.COLOR_BGR2GRAY))
```

## Commands

- Use the SPACE bar to play or pause the video.
- Use the ⬅️ or ➡️ keys to move one frame backward or forward, respectively.
- Use the ⬇️ or ⬆️ keys to move the first or last frame, respectively.

## Credits

- Video by cottonbro studio from Pexels:
https://www.pexels.com/video/man-in-denim-jacket-riding-his-fixie-bicycle-passing-by-5911716/.
It's free to use.
