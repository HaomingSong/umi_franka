from realsense_camera import MultiCamera
import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode
import os
import copy


def capture_video():
    multi_camera = MultiCamera()
    ts_frames = []
    
    while True:
        images = multi_camera.get_frame()
        rgb, depth = images["213522070137"]
        recv_time = time.time_ns()
        qr_time, mask_frame = scan_qr_and_mask(copy.deepcopy(rgb))
        print(f"recv_time: {recv_time}, qr_time: {qr_time}")
        cv2.imshow("rgb", rgb)

        ts_frame = dict(recv_time=recv_time, qr_time=qr_time)
        ts_frames.append(ts_frame)
        
        cv2.imshow("rgb", np.vstack([rgb, mask_frame]))

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果按下 'q' 键则退出循环
            break
        
    return ts_frames
        

def scan_qr_and_mask(frame):
    # 识别图像中的二维码
    decoded_objects = decode(frame)
    qr_data = []
    
    # 遍历所有识别到的二维码
    for obj in decoded_objects:
        # 获取二维码数据
        qr_data.append(obj.data.decode("utf-8"))
        # 获取二维码的位置
        points = obj.polygon
        # 如果二维码被检测到，绘制一个黑色矩形来掩盖二维码
        if points:
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.fillPoly(frame, [pts], color=(0, 0, 0))
    
    return qr_data, frame

def main():
    ts_frames = capture_video()
    with open(f"{os.path.dirname(__file__)}/ts_frame.txt", "w") as f:
        f.write("recv_time, qr_time\n")
        for ts_frame in ts_frames:
            f.write(f"{ts_frame['recv_time']}, {ts_frame['qr_time']}\n")
            
if __name__ == "__main__":
    main()