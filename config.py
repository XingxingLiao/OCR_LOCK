# API + MQTT + 路径配置
url = "https://api.ocr.space/parse/image"
api_key = "K87912659088957"
image_path = "/home/CITSEM/ocr/OCR_LOCK/image/image_000.jpg"

mqtt_broker = "138.100.58.174"
mqtt_port = 1883
mqtt_topic = "ocr/data"

crop_coordinates = [
    (409, 624, 245, 112),   # Region 1
    (781, 612, 209, 118),   # Region 2
    (430, 895, 545, 631)    # Region 3
]
