import subprocess
import psutil
import matplotlib.pyplot as plt
import time

def run_stress_test(duration=60):
    # Start stress test in the background
    stress_process = subprocess.Popen(["stress", "--cpu", "4", "--io", "2", "--timeout", str(duration)])

    # Collect CPU usage, temperature, and voltage data
    cpu_usages = []
    temperatures = []
    voltages = []
    timestamps = []

    start_time = time.time()
    end_time = start_time + duration

    print("Stress test started...")

    while time.time() < end_time:
        # Measure CPU usage
        cpu_usage = psutil.cpu_percent()
        cpu_usages.append(cpu_usage)

        # Measure temperature (assumed to be in degrees Celsius)
        temperature_output = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True)
        temperature = float(temperature_output.stdout.strip().split('=')[1].split('\'')[0])
        temperatures.append(temperature)

        # Measure voltage (assumed to be in volts)
        voltage_output = subprocess.run(["vcgencmd", "measure_volts", "core"], capture_output=True, text=True)
        voltage = float(voltage_output.stdout.strip().split('=')[1].split('V')[0])
        voltages.append(voltage)

        timestamps.append(time.time() - start_time)

        # Sleep for a short interval
        time.sleep(1)

    print("Stress test completed.")

    # Terminate the stress test process
    stress_process.terminate()

    return timestamps, cpu_usages, temperatures, voltages

def plot_metrics(timestamps, cpu_usages, temperatures, voltages):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(timestamps, cpu_usages, label='CPU Usage (%)', color='blue')
    ax1.set_ylabel('CPU Usage (%)')
    ax1.set_title('System Metrics During Stress Test')
    ax1.grid(True)
    ax1.legend()

    ax2.plot(timestamps, temperatures, label='Temperature (°C)', color='red')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Temperature (°C)')
    ax2.grid(True)
    ax2.legend()

    ax2b = ax2.twinx()
    ax2b.plot(timestamps, voltages, label='Voltage (V)', color='green')
    ax2b.set_ylabel('Voltage (V)')
    ax2b.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    timestamps, cpu_usages, temperatures, voltages = run_stress_test()
    plot_metrics(timestamps, cpu_usages, temperatures, voltages)
