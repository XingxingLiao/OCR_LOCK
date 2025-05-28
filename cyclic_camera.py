import os
import time
import threading
from picamera2 import Picamera2

class CyclicCameraCapture(threading.Thread):
    

    def __init__(self, save_dir, max_files=100, interval=300, file_lock=None):
        super().__init__()
        self.save_dir = save_dir
        self.max_files = max_files
        self.interval = interval
        self.running = True
        self.file_lock = file_lock or threading.Lock()

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.picam2 = Picamera2()

        # 创建拍照配置，设置分辨率为 3280x2464
        config = self.picam2.create_still_configuration(main={"size": (3280, 2464)})
        self.picam2.configure(config)

        self.picam2.start()

    def shift_files(self):
        # 移动文件编号，操作需加锁
        with self.file_lock:
            for i in reversed(range(self.max_files - 1)):
                src = os.path.join(self.save_dir, f"image_{i:03d}.jpg")
                dst = os.path.join(self.save_dir, f"image_{i + 1:03d}.jpg")
                if os.path.exists(src):
                    os.rename(src, dst)

    def run(self):
        while self.running:
            self.shift_files()  # 文件移动加锁保护

            filename = os.path.join(self.save_dir, "image_000.jpg")
            with self.file_lock:  # 写文件前加锁
                self.picam2.capture_file(filename)

            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Captured: {filename}")
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.picam2.stop()
        print("Camera thread stopped.")
