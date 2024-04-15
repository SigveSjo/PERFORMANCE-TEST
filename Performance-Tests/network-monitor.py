import subprocess
import matplotlib.pyplot as plt
import time

def measure_network_performance(interval=10, duration=300):
    timestamps = []
    download_speeds = []
    upload_speeds = []
    pings = []

    start_time = time.time()
    end_time = start_time + duration

    print("Network performance measurement started...")

    while time.time() < end_time:
        # Run speedtest-cli to measure network performance
        speedtest_output = subprocess.run(["speedtest-cli", "--simple"], capture_output=True, text=True)
        output_lines = speedtest_output.stdout.splitlines()

        # Extract download speed, upload speed, and ping
        for line in output_lines:
            if "Download" in line:
                download_speed = float(line.split()[1])
            elif "Upload" in line:
                upload_speed = float(line.split()[1])
            elif "Ping" in line:
                ping = float(line.split()[1])

        # Append measurements to lists
        timestamps.append(time.time() - start_time)
        download_speeds.append(download_speed)
        upload_speeds.append(upload_speed)
        pings.append(ping)

        # Sleep for the specified interval before the next measurement
        time.sleep(interval)

    print("Network performance measurement completed.")

    # Plot the results
    plt.figure(figsize=(10, 6))

    plt.subplot(3, 1, 1)
    plt.plot(timestamps, download_speeds, label='Download Speed (Mbps)', color='blue')
    plt.ylabel('Download Speed (Mbps)')
    plt.title('Network Performance')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(timestamps, upload_speeds, label='Upload Speed (Mbps)', color='green')
    plt.ylabel('Upload Speed (Mbps)')
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(timestamps, pings, label='Ping (ms)', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Ping (ms)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    measure_network_performance()

