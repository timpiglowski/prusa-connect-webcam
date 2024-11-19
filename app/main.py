import os
import time
import cv2
import requests
import urllib3
import logging

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
def capture_image(output_path):
    max_retries = 3
    retry_delay = 2

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
            return

        except Exception as e:
            logger.error(f"Camera error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

def main():
    while True:
        try:
            output_path = '/tmp/output.jpg'
            capture_image(output_path)

            headers = {
                'accept': '*/*',
                'content-type': 'image/jpg',
                'fingerprint': FINGERPRINT,
                'token': CAMERA_TOKEN
            }

            with open(output_path, 'rb') as image_file:
                response = requests.put(
                    HTTP_URL,
                    headers=headers,
                    data=image_file,
                    verify=False
                )

            logger.info(f'Image uploaded successfully. Next capture in {DELAY_SECONDS}s')
            delay = DELAY_SECONDS

        except Exception as e:
            logger.error(f"Error occurred: {str(e)}, retrying after {LONG_DELAY_SECONDS}s")
            delay = LONG_DELAY_SECONDS

        time.sleep(delay)

if __name__ == '__main__':
    main()
