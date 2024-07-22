from realsense_camera import MultiCamera
import cv2
import numpy as np
import time
if __name__ == "__main__":
    multi_camera = MultiCamera()
    camera_ids = list(multi_camera.cameras.keys())
    
    while True:
            images = multi_camera.get_frame()
            rgb, depth = images["213522070137"]
            recv_time = time.time_ns()            
            # cv2.imshow("rgb", np.hstack([rgb, mask_frame]))
            cv2.imshow("rgb", rgb)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果按下 'q' 键则退出循环
                break
        