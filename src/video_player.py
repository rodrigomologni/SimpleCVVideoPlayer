# -*- coding: utf-8 -*-

import os.path
import time

import cv2 as cv


class LSize:
    """Landscape standard sizes."""
    SD = (720, 480)
    HD = (1280, 720)
    FHD = (1920, 1080)


class PSize:
    """Portrait standard sizes."""
    SD = (480, 720)
    HD = (720, 1280)
    FHD = (1080, 1920)


class Color:
    """RGB colors."""
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Key:
    """Keyboard key codes."""
    SPACE = 32
    ARROW_LEFT = 2424832
    ARROW_RIGHT = 2555904
    ARROW_UP = 2490368
    ARROW_DOWN = 2621440


def convert_to_clock(milliseconds):
    """Converts time from milliseconds to digital clock format.

    Parameters
    ----------
    milliseconds : int or float
        Time in milliseconds.

    Returns
    -------
    str
        Time in digital clock format.
    """
    milliseconds = int(milliseconds)
    hours = milliseconds // 3600000
    milliseconds %= 3600000
    minutes = milliseconds // 60000
    milliseconds %= 60000
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}'


class VideoPlayer:
    """Simple OpenCV video player.

    Attributes
    ----------
    filename : str
        Path to video.
    title : str, default='Video Player'
        Window name.
    """
    font_face = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    def __init__(self, filename, title='Video Player'):
        self._video = cv.VideoCapture(filename)
        self._video.set(cv.CAP_PROP_ORIENTATION_AUTO, 1)

        self._winname = str(int(time.time()))
        cv.namedWindow(self._winname, cv.WINDOW_NORMAL)
        cv.setWindowTitle(self._winname, f'{os.path.basename(filename)} - {title}')
        cv.resizeWindow(self._winname,
                        int(self._video.get(cv.CAP_PROP_FRAME_WIDTH)),
                        int(self._video.get(cv.CAP_PROP_FRAME_HEIGHT)))

    @property
    def video(self):
        """Returns the instance of `cv.VideoCapture` created when `VideoPlayer` was instantiated."""
        return self._video

    @property
    def winname(self):
        """Returns the window name."""
        return self._winname

    def resize(self, size):
        """Resizes the window.

        Parameters
        ----------
        size : (int, int)
            Window width and height.
        """
        cv.resizeWindow(self._winname, size)

    def _put_text(self, image, text):
        (w, h), _ = cv.getTextSize(text, self.font_face, self.font_scale, self.font_thickness)
        pt1 = (0, 0)
        pt2 = (w + 20, h + 20)
        cv.rectangle(image, pt1, pt2, Color.BLACK, -1)
        org = (10, h + 10)
        cv.putText(image, text, org, self.font_face, self.font_scale, Color.WHITE, self.font_thickness)

    def prep(self, callback):
        """Applies the callback function to the first frame.

        Parameters
        ----------
        callback : function
            A callback function that receives an OpenCV image.
        """
        self._video.set(cv.CAP_PROP_POS_FRAMES, 0)
        _, image = self._video.read()
        callback(image)

    def run(self, callback=None, start=None):
        """Loads and displays the video by applying the callback function to the frames.

        Parameters
        ----------
        callback : function, optional
            A callback function that receives and returns an OpenCV image.
        start : int, optional.
            Video start time, in milliseconds.
        """
        num_frames = int(self._video.get(cv.CAP_PROP_FRAME_COUNT))
        fps = self._video.get(cv.CAP_PROP_FPS)
        delay = 0

        if start:
            self._video.set(cv.CAP_PROP_POS_MSEC, start)

        while cv.getWindowProperty(self._winname, cv.WND_PROP_VISIBLE) == 1:
            retval, image = self._video.read()
            index = int(self._video.get(cv.CAP_PROP_POS_FRAMES))

            if retval:
                timer = cv.getTickCount()
                if callback: image = callback(image)
                cv_fps = cv.getTickFrequency() / (cv.getTickCount() - timer)
                msec = self._video.get(cv.CAP_PROP_POS_MSEC)
                text = f'{convert_to_clock(msec)} ({index:03}/{num_frames:03}) {cv_fps:.1f} FPS'
                self._put_text(image, text)
                cv.imshow(self._winname, image)
            else:
                delay = 0

            while cv.getWindowProperty(self._winname, cv.WND_PROP_VISIBLE) == 1:
                key = cv.waitKeyEx(delay)
                if key == Key.SPACE:
                    delay = 0 if delay > 0 else int(1000 / fps)
                    if index >= num_frames: self._video.set(cv.CAP_PROP_POS_FRAMES, 0)
                    break
                if key == Key.ARROW_LEFT:
                    delay = 0
                    self._video.set(cv.CAP_PROP_POS_FRAMES, index - 2)
                    break
                if key == Key.ARROW_RIGHT:
                    delay = 0
                    break
                if key == Key.ARROW_DOWN:
                    delay = 0
                    self._video.set(cv.CAP_PROP_POS_FRAMES, 0)
                    break
                if key == Key.ARROW_UP:
                    delay = 0
                    self._video.set(cv.CAP_PROP_POS_FRAMES, num_frames - 1)
                    break
                if delay > 0: break

        self._video.release()


def example_callback():
    player = VideoPlayer('../videos/5911716-hd_1920_1080_25fps.mp4')
    player.resize(LSize.SD)
    player.run(lambda image: cv.cvtColor(image, cv.COLOR_BGR2GRAY))


def example_start():
    player = VideoPlayer('../videos/5911716-hd_1920_1080_25fps.mp4')
    player.resize(LSize.SD)
    player.run(start=1000)


if __name__ == '__main__':
    example_start()
