import os
import time
import cv2
import requests
import urllib3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Environment variables with defaults
HTTP_URL = os.getenv('HTTP_URL', 'https://connect.prusa3d.com/c/snapshot')
DELAY_SECONDS = int(os.getenv('DELAY_SECONDS', 10))
LONG_DELAY_SECONDS = int(os.getenv('LONG_DELAY_SECONDS', 60))
FINGERPRINT = os.getenv('FINGERPRINT', '123456789012345678')
CAMERA_TOKEN = os.getenv('CAMERA_TOKEN', 'mvq1Q9dXC3lvDDTDgQ9U')
CAMERA_RESOLUTION = (2274, 1280)
IMAGES_DIR = '/app/camera_images'

def ensure_directory():
    os.makedirs(IMAGES_DIR, exist_ok=True)

def capture_image():
    max_retries = 3
    retry_delay = 2
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(IMAGES_DIR, f'capture_{timestamp}.jpg')

    for attempt in range(max_retries):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise RuntimeError(f"Failed to open camera (attempt {attempt + 1}/{max_retries})")

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_RESOLUTION[0])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_RESOLUTION[1])

            ret, frame = cap.read()
            if not ret or frame is None:
                raise RuntimeError("Failed to capture image")

            cv2.imwrite(output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            cap.release()
            return output_path

        except Exception as e:
            logger.error(f"Camera error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

def main():
    ensure_directory()

    while True:
        try:
            image_path = capture_image()

            headers = {
                'accept': '*/*',
                'content-type': 'image/jpg',
                'fingerprint': FINGERPRINT,
                'token': CAMERA_TOKEN
            }

            with open(image_path, 'rb') as image_file:
                response = requests.put(
                    HTTP_URL,
                    headers=headers,
                    data=image_file,
                    verify=False
                )

            os.remove(image_path)
            logger.info(f'Image uploaded successfully. Next capture in {DELAY_SECONDS}s')
            delay = DELAY_SECONDS

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}, retrying after {LONG_DELAY_SECONDS}s")
            delay = LONG_DELAY_SECONDS

        time.sleep(delay)

if __name__ == '__main__':
    main()
