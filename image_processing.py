import cv2
import os

def preprocess_image(image_path, crop_coords, save_path):
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return False

    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Failed to load image: {image_path}")
        return False

    x, y, w, h = crop_coords
    img_h, img_w = image.shape[:2]
    if x + w > img_w or y + h > img_h:
        print(f"[ERROR] Invalid crop region {crop_coords}, image size: {img_w}x{img_h}")
        return False

    cropped = image[y:y+h, x:x+w]
    if cropped.size == 0:
        print(f"[ERROR] Cropped image is empty.")
        return False

    denoised = cv2.fastNlMeansDenoising(cropped, None, 30, 7, 21)
    cv2.imwrite(save_path, denoised)
    return True

