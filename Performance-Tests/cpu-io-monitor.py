import subprocess
import re
import psutil
import matplotlib.pyplot as plt
import time

def run_hdparm(device):
    # Run hdparm command to measure disk read speed
    read_speed_output = subprocess.run(["sudo", "hdparm", "-t", device], capture_output=True, text=True)
    # Extract read speed from the output
    read_speed_match = re.search(r"([\d.]+) MB/sec", read_speed_output.stdout)
    read_speed = float(read_speed_match.group(1)) if read_speed_match else None

    # Run hdparm command to measure disk write speed
    write_speed_output = subprocess.run(["sudo", "hdparm", "-Tt", device], capture_output=True, text=True)
    # Extract write speed from the output
    write_speed_match = re.search(r"([\d.]+) MB/sec", write_speed_output.stdout)
    write_speed = float(write_speed_match.group(1)) if write_speed_match else None

    return read_speed, write_speed

def plot_disk_performance(read_speeds, write_speeds):
    plt.plot(read_speeds, label='Read Speed')
    plt.plot(write_speeds, label='Write Speed')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (MB/sec)')
    plt.title('Disk I/O Performance')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    disk_device = "/dev/sda"  # Change this to your disk device

    read_speeds = []
    write_speeds = []
    cpu_usages = []

    start_time = time.time()
    duration = 60  # Run for 60 seconds
    end_time = start_time + duration

    while time.time() < end_time:
        read_speed, write_speed = run_hdparm(disk_device)
        read_speeds.append(read_speed)
        write_speeds.append(write_speed)

        cpu_usage = psutil.cpu_percent(interval=1)  # Monitor CPU usage every second
        cpu_usages.append(cpu_usage)

    plot_disk_performance(read_speeds, write_speeds)

    plt.plot(cpu_usages)
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.show()

