import time
import keyboard

from screenshot import ScreenshotGenerator
from timer import RepeatedTimer


def schedule(sec, callback, **kwargs):
    time.sleep(sec)
    callback(**kwargs)


def take_screenshot_5s(ssg):
    def screenshot_and_save(ssg):
        ss = ssg.grab_screen()
        current_time = time.strftime("%m-%d_%H-%M-%S", time.gmtime())
        ssg.save_image(ss, f"SCR_{current_time}.png")

    rt = RepeatedTimer(5, screenshot_and_save, ssg)

    def cleanup(_):
        print("Cleaning up")
        rt.stop()

    keyboard.on_press_key("q", cleanup)


if __name__ == "__main__":
    ssg = ScreenshotGenerator(resolution=(1920, 1080))
    take_screenshot_5s(ssg)
