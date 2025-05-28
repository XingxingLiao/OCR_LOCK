import cv2

def preprocess_image(image_path, crop_coords, processed_image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Failed to read the image.")
        return None

    x, y, w, h = crop_coords
    cropped = image[y:y+h, x:x+w]
    denoised = cv2.fastNlMeansDenoising(cropped, None, 30, 7, 21)
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(processed_image_path, binary)
    return processed_image_path
