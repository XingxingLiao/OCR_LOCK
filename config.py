# API + MQTT + 路径配置
url = "https://api.ocr.space/parse/image"
api_key = "K87912659088957"
image_path = "/home/CITSEM/Ocr_Project/OCR_MQTT/Orignal_Image/whatsapp_image_2025-03-20_at_11.55.55.jpeg"

mqtt_broker = "138.100.58.174"
mqtt_port = 1883
mqtt_topic = "test/message"

crop_coordinates = [
    (409, 624, 245, 112),   # Region 1
    (781, 612, 209, 118),   # Region 2
    (430, 895, 545, 631)    # Region 3
]
