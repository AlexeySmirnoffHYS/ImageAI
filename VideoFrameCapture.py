import cv2

def capture_frame(url, output_filename):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Failed to open video stream.")
        return
    
    ret, frame = cap.read()
    if ret:
        # Сохраняем кадр в файл
        cv2.imwrite(output_filename, frame)
        print(f"Frame saved to: {output_filename}")
    
    cap.release()
