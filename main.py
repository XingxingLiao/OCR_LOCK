from camera_capture.cyclic_camera import CyclicCameraCapture
from image_processing.preprocess import preprocess_image
from ocr_api.client import send_to_ocr_api
from postprocessing.postprocess import extract_numbers, extract_on_off
from mqtt_publisher.publisher import send_mqtt_message
from config import image_path, crop_coordinates

import threading
import time
import json

def run_ocr_and_publish(file_lock):
    with file_lock:
        # 省略 OCR 处理代码，跟之前示例一样
        pass

if __name__ == "__main__":
    save_path = "/home/pi/camera_images"
    file_lock = threading.Lock()

    camera_thread = CyclicCameraCapture(save_path, max_files=100, interval=300, file_lock=file_lock)
    camera_thread.start()

    try:
        while True:
            run_ocr_and_publish(file_lock)
            time.sleep(60)
    except KeyboardInterrupt:
        camera_thread.stop()
        camera_thread.join()
