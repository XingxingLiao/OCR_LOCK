from cyclic_camera import CyclicCameraCapture
from image_processing import preprocess_image
from ocr_api import send_to_ocr_api
from postprocessing import extract_numbers, extract_on_off
from mqtt_publisher import send_mqtt_message
from config import image_path, crop_coordinates

import threading
import time
import json

def run_ocr_and_publish(file_lock):
    with file_lock:
        all_results = []
        on_off_results = []

        for i, coords in enumerate(crop_coordinates):
            region_id = i + 1
            processed_path = f"/home/CITSEM/OCR_LOCK/processed_photo/processed_region_{region_id}.jpeg"

            if preprocess_image(image_path, coords, processed_path):
                response = send_to_ocr_api(processed_path)
                if response.status_code == 200:
                    result = response.json()
                    if not result.get("IsErroredOnProcessing"):
                        text = result["ParsedResults"][0]["ParsedText"]
                        print(f"[DEBUG] Region {region_id} OCR Text:\n{text}")
                        if region_id <= 2:
                            all_results.extend(extract_numbers(text, region_id))
                        else:
                            on_off_results.extend(extract_on_off(text, region_id))
                    else:
                        print(f"[ERROR] Region {region_id} OCR Error: {result.get('ErrorMessage')}")
                else:
                    print(f"[ERROR] Region {region_id} API HTTP Error: {response.status_code}")

        # Build a flat dictionary message with default 2 number regions and 3 on/off regions
        def build_flat_message(all_results, on_off_results, max_num_regions=2, max_onoff_regions=3):
            message = {"status": "success"}

            # Process numeric regions (Region 1 and 2)
            for region_id in range(1, max_num_regions + 1):
                value = "NO TEXT"
                for item in all_results:
                    if f"Region {region_id} -" in item:
                        value = item.split(" - ")[1]
                        break
                message[f"Region_{region_id}"] = value

            # Process on/off regions (Region 3_1, 3_2, 3_3)
            for idx in range(1, max_onoff_regions + 1):
                value = "NO TEXT"
                prefix = "Region 3 - "
                for item in on_off_results:
                    if prefix in item and f"#{idx}" in item:
                        value = item.split(" - ")[1].split("#")[0].strip()
                        break
                message[f"Region_3_{idx}"] = value

            return message

        mes = build_flat_message(all_results, on_off_results)
        send_mqtt_message(mes)
        print(mes)
if __name__ == "__main__":
    save_path = "/home/CITSEM/OCR_LOCK/image"
    file_lock = threading.Lock()

    camera_thread = CyclicCameraCapture(save_path, max_files=100, interval=10, file_lock=file_lock)
    camera_thread.start()

    try:
        while True:
            run_ocr_and_publish(file_lock)
            time.sleep(60)
    except KeyboardInterrupt:
        camera_thread.stop()
        camera_thread.join()

