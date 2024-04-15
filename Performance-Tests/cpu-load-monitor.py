import psutil
import time
import matplotlib.pyplot as plt

def stability_test(duration=10):
    start_time = time.time()
    end_time = start_time + duration

    cpu_usages = []
    timestamps = []

    print("Stability test started...")
    while time.time() < end_time:
        # Perform CPU-intensive task (e.g., calculate prime numbers)
        prime_number = 9999991
        for i in range(2, int(prime_number ** 0.5) + 1):
            if prime_number % i == 0:
                break

        # Monitor system resources (optional)
        cpu_usage = psutil.cpu_percent()
        cpu_usages.append(cpu_usage)
        timestamps.append(time.time() - start_time)

        # Sleep for a short interval to avoid consuming too much CPU
        time.sleep(0.1)

    print("Stability test completed.")

    # Plot CPU usage over time
    plt.plot(timestamps, cpu_usages)
    plt.xlabel('Time (s)')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage During Stability Test')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    stability_test()

