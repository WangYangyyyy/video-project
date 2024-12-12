import cv2
import threading
import time
import os

# 摄像头地址列表
camera_urls = [
    'rtsp://admin:admin@10.250.7.20/1',
]

# 目标文件夹
output_folder = 'G:\\Project\\Video\\pythonProject\\picture'
os.makedirs(output_folder, exist_ok=True)


def capture_images(camera_urls, output_folder):
    while True:
        for camera_url in camera_urls:
            cap = cv2.VideoCapture(camera_url)
            if not cap.isOpened():
                print(f"Error: Could not open video stream from {camera_url}")
                continue

            ret, frame = cap.read()
            if not ret:
                print(f"Error: Could not read frame from {camera_url}")
                cap.release()
                continue

            # 获取当前时间戳
            timestamp = int(time.time())
            # 构建图像文件名
            image_filename = os.path.join(output_folder, f"{camera_url.split('/')[-1]}_{timestamp}.jpg")
            # 保存图像
            cv2.imwrite(image_filename, frame)
            print(f"Saved image: {image_filename}")

            cap.release()

        # 每隔10秒截取一次图像
        time.sleep(10)


# 创建并启动线程
thread = threading.Thread(target=capture_images, args=(camera_urls, output_folder))
thread.start()
thread.join()
