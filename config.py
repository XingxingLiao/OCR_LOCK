# API + MQTT + 路径配置
url = "https://api.ocr.space/parse/image"
api_key = "K87912659088957"
image_path = "/home/CITSEM/ocr/OCR_LOCK/image/image_000.jpg"

# mqtt_broker = "138.100.58.174"
# mqtt_port = 1883
# mqtt_topic = "ocr/data"

mqtt_broker = "0eb00aca75ab4f56b36f74924b54b76b.s1.eu.hivemq.cloud" 
mqtt_port = 8883
mqtt_topic = "ocr/data"
mqtt_username = "CITSEM"
mqtt_password = "Admin123"

crop_coordinates = [
    (409, 624, 245, 112),   # Region 1
    (781, 612, 209, 118),   # Region 2
    (430, 895, 545, 631)    # Region 3
]
