import keyboard
import numpy as np
from PIL import Image

from screenshot import ScreenshotGenerator
from timer import RepeatedTimer

ssg = ScreenshotGenerator()


def image_diff(img1, img2):
    assert img1.shape == img2.shape, "The two images do not have the same shape"
    return np.count_nonzero(img1 != img2) / img1.size


def generate_slides(images, threshold=0.06, num_attempts=0):
    # Select the images that should be included in the slides
    slides = []
    for i in range(1, len(images)):
        diff = image_diff(images[i - 1], images[i])
        if diff > threshold:
            slides.append(images[i - 1])
            print(f"A {diff:.4f}")
        else:
            print(f"R {diff:.4f}")

    # Convert the images into PIL format images
    slides = [img[:, :, ::-1] for img in slides]  # BGR -> RGB
    pil_images = [Image.fromarray(img.astype("uint8"), "RGB") for img in slides]

    # Generate the slides as a PDF form
    pdf_filename = "slides.pdf"

    if len(pil_images) >= 2:
        pil_images[0].save(pdf_filename,
                           "PDF",
                           resolution=100.0,
                           save_all=True,
                           append_images=pil_images[1:])
    else:
        if num_attempts < 3:
            threshold /= 3
            print(f"Not enough images with the current threshold, trying again \
                with threshold = {threshold:.4f}...")
            return generate_slides(images,
                                   threshold,
                                   num_attempts=num_attempts + 1)
        else:
            print("Too many attempts, no PDF generated")

    return len(slides)


def main():
    screenshots = []
    rt = RepeatedTimer(5, lambda: screenshots.append(ssg.grab_screen()))

    def cleanup(_):
        # Take a final screenshot at the end as a dummy screenshot
        screenshots.append(ssg.grab_screen())

        # Process the screenshots and attempt to generate slides
        print(f"Initial processing of {len(screenshots)} images.")
        num_final_images = generate_slides(screenshots)
        print(f"Final count of images used in PDF: {num_final_images}")

        # Stop the repeating timer for the screenshots
        rt.stop()

    keyboard.on_press_key("q", cleanup)


if __name__ == "__main__":
    main()
