import psutil
import time
import matplotlib.pyplot as plt

def monitor_cpu(interval=1, duration=10):
    cpu_usage = []
    timestamps = []
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        cpu_percent = psutil.cpu_percent(interval=interval)
        cpu_usage.append(cpu_percent)
        timestamps.append(time.time() - start_time)
        time.sleep(interval)

    plt.plot(timestamps, cpu_usage)
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    monitor_cpu()

