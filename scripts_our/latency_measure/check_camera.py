from realsense_camera import MultiCamera
import cv2
import numpy as np
import time
if __name__ == "__main__":
    multi_camera = MultiCamera()
    camera_ids = list(multi_camera.cameras.keys())
    
    while True:
            # Get img info
        images = multi_camera.get_frame()
        rgbs = []
        for camera_id in camera_ids:
            rgb, depth = images[camera_id]
            rgbs.append(rgb)
        
        cv2.imshow("rgb", np.hstack(rgbs))
        cv2.waitKey(1)
        
        time.sleep(0.1)
        