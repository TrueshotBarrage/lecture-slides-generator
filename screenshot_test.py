import time
import keyboard

from screenshot import ScreenshotProcessing
from timer import RepeatedTimer

if __name__ == "__main__":
    ssp = ScreenshotProcessing()
    print("Starting to record")
    ssp.start_recording_screen()
    time.sleep(22)
    print("Stopping recording")
    ssp.stop_recording_screen()
