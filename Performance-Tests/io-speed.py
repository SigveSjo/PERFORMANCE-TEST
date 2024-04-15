import subprocess
import re
import matplotlib.pyplot as plt

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

def plot_disk_performance(read_speed, write_speed):
    labels = ['Read Speed', 'Write Speed']
    speeds = [read_speed, write_speed]

    plt.bar(labels, speeds, color=['blue', 'green'])
    plt.ylabel('Speed (MB/sec)')
    plt.title('Disk I/O Performance')
    plt.show()

if __name__ == "__main__":
    disk_device = "/dev/sda"  # Change this to your disk device

    read_speed, write_speed = run_hdparm(disk_device)

    if read_speed is not None and write_speed is not None:
        print(f"Read Speed: {read_speed} MB/sec")
        print(f"Write Speed: {write_speed} MB/sec")
        
        plot_disk_performance(read_speed, write_speed)
    else:
        print("Error: Failed to retrieve disk I/O performance.")

