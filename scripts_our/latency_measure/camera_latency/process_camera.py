import os
from datetime import datetime

def process_data():
    with open(f"{os.path.dirname(__file__)}/ts_frame.txt", "r") as f:
        lines = f.readlines()
        ts_frames = []
        for line in lines[1:]:
            recv_time_str, qr_time_str = line.strip().split(",")
            if qr_time_str.strip() == '[]':
                continue
            qr_time_str = '20' + qr_time_str[4:-2]
            
            dt = datetime.strptime(qr_time_str, "%Y%m%d%H%M%S.%f")
            qr_seconds_since_epoch = dt.timestamp()
            qr_time = int(qr_seconds_since_epoch * 1e9)
            recv_time = int(recv_time_str)
            
            print(recv_time, qr_time, (recv_time-qr_time)*1e-9)
            ts_frames.append(dict(recv_time=recv_time, qr_time=qr_time, latency=(recv_time-qr_time)*1e-9))
            
    latency_sum = 0
    for ts_frame in ts_frames:
        latency_sum += ts_frame['latency']
    print(f"Average latency: {latency_sum/len(ts_frames)}")
            
if __name__ == "__main__":
    process_data()