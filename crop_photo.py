import cv2

# Global variables
crop_params = []  # Stores crop areas (x, y, w, h)
current_boxes = []  # Stores the boxes drawn by mouse (for real-time display)
start_x, start_y, cropping = -1, -1, False
current_image = None  # The current image (original image)

def crop_callback(event, x, y, flags, param):
    global crop_params, start_x, start_y, cropping, current_image, current_boxes

    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True
        start_x, start_y = x, y  # Record the starting coordinates on the image
        current_boxes.append(("temp", (x, y, 0, 0)))  # Add a temporary box for real-time display

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            if current_boxes and current_boxes[-1][0] == "temp":
                current_boxes[-1] = ("temp", (start_x, start_y, x - start_x, y - start_y))
                # Display in real-time on the original image
                temp_image = current_image.copy()
                for box in current_boxes:
                    x1, y1, w, h = box[1]
                    cv2.rectangle(temp_image, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
                cv2.imshow("Image", temp_image)

    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        w, h = x - start_x, y - start_y
        if w > 0 and h > 0:
            crop_params.append((start_x, start_y, w, h))
            print(f"Crop area saved: x={start_x}, y={start_y}, w={w}, h={h}")
            # Convert the temporary box to a permanent box
            current_boxes.pop()  # Remove the temporary box
            current_boxes.append(("saved", (start_x, start_y, w, h)))
        else:
            print("Invalid crop area, not saved")
            current_boxes.pop()

        # Display the image with all the boxes
        temp_image = current_image.copy()
        for box in current_boxes:
            x1, y1, w, h = box[1]
            cv2.rectangle(temp_image, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
        cv2.imshow("Image", temp_image)

# Read the image (original image, no resizing)
image_path = "/home/xingxin/Downloads/whatsapp_image_2025-03-20_at_11.55.55.jpeg"
current_image = cv2.imread(image_path)

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Image", crop_callback)
cv2.imshow("Image", current_image)

print("Please select the crop area with the mouse, press 'q' to quit, press 'ESC' to reset the crop area.")
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == 27:  # Press ESC to reset
        current_image = cv2.imread(image_path)  # Reload the original image
        crop_params = []
        current_boxes = []
        print("All crop areas have been reset")
        cv2.imshow("Image", current_image)

cv2.destroyAllWindows()

# Save the cropped images
if crop_params:
    for idx, (x, y, w, h) in enumerate(crop_params):
        cropped = current_image[y:y+h, x:x+w]
        cv2.imwrite(f"/home/xingxin/Downloads/cropped_image_{idx+1}.jpg", cropped)
