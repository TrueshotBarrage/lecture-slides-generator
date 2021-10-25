from cv2 import cvtColor, COLOR_BGR2RGB, imwrite
from mss import mss
from PIL import Image
from timer import RepeatedTimer
import numpy as np

import os


class ScreenshotProcessingException(Exception):
    """General purpose exception that is raised for various operations going
    wrong with the ScreenshotProcessing module.
    """
    pass


class ScreenshotProcessing:
    """Module to take and process screenshots and generate PDF slides.

    Args:
        resolution (int, int): The width and height of the monitor.

    Class variables:
        sct (MSSBase): Takes captures from the screen
        monitor (dict): The dimensions of the monitor
        screenshots (list): The captured screenshots
        slides (list): The screenshots used for the generated slides
        rt (RepeatedTimer): The timer module that continuously grabs the screen
        path (str): The directory to which to save the generated slides
    """
    def __init__(self, resolution=(1920, 1080)):
        self.sct = mss()
        self.monitor = {
            "left": 0,
            "top": 0,
            "width": resolution[0],
            "height": resolution[1]
        }
        self.screenshots = []
        self.slides = []
        self.rt = None
        self.path = None

    def start_recording_screen(self, interval=5):
        """Start a timer to snapshot the screen periodically.

        Args:
            interval (int): How often a screenshot will be taken
        """
        if self.rt is None:
            self.rt = RepeatedTimer(
                interval, lambda: self.screenshots.append(self.grab_screen()))
        else:
            raise ScreenshotProcessingException("Already recording!")

    def stop_recording_screen(self):
        """Clean up the processes and process the images."""
        if self.rt is not None:
            # Stop the repeating timer for the screenshots
            self.rt.stop()
            self.rt = None

            # Take a final screenshot at the end as a dummy screenshot
            self.screenshots.append(self.grab_screen())

            # Process the screenshots and attempt to generate slides
            print(f"Initial processing of {len(self.screenshots)} images.")
            self.generate_slides(self.screenshots)
            print(f"Final count of images used in PDF: {len(self.slides)}")

            # Destroy the screenshots
            self.screenshots = self.slides = []

        else:
            raise ScreenshotProcessingException(
                "Cannot stop recording when not recording!")

    def grab_screen(self):
        """Take a screenshot from the monitor.

        Returns:
            np.ndarray: The numpy array that represents the RGB image data
        """
        screenshot = self.sct.grab(self.monitor)
        img = np.array(screenshot)
        img = cvtColor(img, COLOR_BGR2RGB)

        return img

    def image_diff(self, img1, img2):
        """Return the percent diff between the two image arrays.
        Args:
            img1 (np.ndarray): The first image numpy array
            img2 (np.ndarray): The second image numpy array

        Returns:
            float: The percent difference of the two arrays    
        """
        assert img1.shape == img2.shape, "The two images do not have the same shape"
        return np.count_nonzero(img1 != img2) / img1.size

    def generate_slides(self, images, threshold=0.06, num_attempts=1):
        """Generate the lecture slides from a list of screenshots of the video
        lecture, using a specified threshold that determines whether images are 
        "equal," i.e. similar enough to the previous image.

        Args:
            images (list): List of screenshots to be processed
            threshold (float): The threshold for screenshots to be deemed similar.
            If the two images compared have at least threshold percentage of their
            pixel data equal, then they are considered equal and therefore accepted.
            num_attempts (int): The number of times this function has been run
        """
        # Select the images that should be included in the slides
        for i in range(1, len(images)):
            diff = self.image_diff(images[i - 1], images[i])
            if diff > threshold:
                self.slides.append(images[i - 1])
                print(f"A {diff:.4f}")
            else:
                print(f"R {diff:.4f}")

        # Convert the images into PIL format images
        pil_images = [
            Image.fromarray(img.astype("uint8"), "RGB") for img in self.slides
        ]

        # Generate the slides as a PDF form
        if self.path:
            pdf_filename = os.path.join(self.path, "slides.pdf")
        else:
            raise ScreenshotProcessingException(
                "Cannot write the PDF to an empty directory!")

        # Only generate the slides if there are enough images to work with
        if len(pil_images) >= 2:
            pil_images[0].save(pdf_filename,
                               "PDF",
                               resolution=100.0,
                               save_all=True,
                               append_images=pil_images[1:])

        # Not enough images, maybe we need a lower acceptance threshold
        else:
            if num_attempts < 3:
                threshold /= 3
                print(
                    f"Not enough images with the current threshold, trying again"
                    f"with threshold = {threshold:.4f}...")
                return self.generate_slides(images,
                                            threshold,
                                            num_attempts=num_attempts + 1)
            else:
                print("Too many attempts, no PDF generated")
