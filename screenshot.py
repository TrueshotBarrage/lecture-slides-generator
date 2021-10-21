import cv2
from mss import mss
import numpy as np


class ScreenshotGenerator:
    def __init__(self, resolution=(1920, 1080)):
        self.sct = mss()
        self.monitor = {
            "left": 0,
            "top": 0,
            "width": resolution[0],
            "height": resolution[1]
        }

    # Take a screenshot from the monitor.
    def grab_screen(self):
        screenshot = self.sct.grab(self.monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Cycle the colors from BGR to RGB
        img = img[:, :, ::-1]

        return img

    def save_image(self, img_array, file_name):
        cv2.imwrite(file_name, img_array)
