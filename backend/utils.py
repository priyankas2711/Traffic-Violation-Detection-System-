import cv2
import time
import os

OUTPUT_FOLDER = "outputs"

def save_violation(frame, violation_type):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    timestamp = int(time.time())
    filename = f"{OUTPUT_FOLDER}/{violation_type}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)

    return filename