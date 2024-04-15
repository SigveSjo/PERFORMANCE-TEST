import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import threading


def perform_prime_number_calculation(prime_number=39916801):
    for i in range(2, int(prime_number ** 0.5) + 1):
        if prime_number % i == 0:
            break

def perform_io_operations():
    # simulating I/O operations
    for _ in range(1000):
        with open("/dev/null", "wb") as null_file:
            for _ in range(1000):
                null_file.write(b"I simulate I/O operations.")

def perform_cpu_memory_intensive_task():
    # creating a large list and performing operations on it
    large_list = [i for i in range(100000)] 
    squared_list = [x**2 for x in large_list] 
    del large_list 
    del squared_list 

def plot_stability(timestamps, cpu_usages, memory_usages, duration):
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    axs[0].plot(timestamps, cpu_usages, label='CPU Usage (%)')
    axs[0].set_ylabel('CPU Usage (%)')
    axs[0].set_title('CPU Usage')
    axs[0].grid(True)
    axs[0].set_ylim(0, 100)
    axs[0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    axs[1].plot(timestamps, memory_usages, label='Memory Usage (%)')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel('Memory Usage (%)')
    axs[1].set_title('Memory Usage')
    axs[1].grid(True)
    axs[1].set_ylim(0, 100)

    legend_patches = [
        Patch(color='orange', alpha=0.1, label='CPU task'),
        Patch(color='blue', alpha=0.1, label='I/O task'),
        Patch(color='green', alpha=0.1, label='CPU+Memory task'),
        Patch(color='red', alpha=0.1, label='All')
    ]

    plt.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.2, -0.1), fancybox=True, shadow=False, ncol=3)

    for ax in axs:
        ax.axvspan(duration/9, 2*duration/9, color='orange', alpha=0.1)
        ax.axvspan(3*duration/9, 4*duration/9, color='blue', alpha=0.1)
        ax.axvspan(5*duration/9, 6*duration/9, color='green', alpha=0.1)
        ax.axvspan(7*duration/9, 8*duration/9, color='red', alpha=0.1)

    plt.tight_layout()
    plt.show()


def stability_test(duration=300):
    start_time = time.time()
    end_time = start_time + duration

    cpu_usages = []
    memory_usages = []
    timestamps = []

    prime_number_condition = lambda timestamp: start_time + duration/9 < timestamp < start_time + 2*duration/9
    io_condition = lambda timestamp: start_time + 3*duration/9 < timestamp < start_time + 4*duration/9
    memory_intensive_condition = lambda timestamp: start_time + 5*duration/9 < timestamp < start_time + 6*duration/9 
    all_tasks_condition = lambda timestamp: start_time + 7*duration/9 < timestamp < start_time + 8*duration/9 

    cpu_thread = threading.Thread(target=perform_prime_number_calculation)
    io_thread = threading.Thread(target=perform_io_operations)
    memory_thread = threading.Thread(target=perform_cpu_memory_intensive_task)

    print("Stability test started...")
    while time.time() < end_time:
        timestamp = time.time()

        if prime_number_condition(timestamp):
            perform_prime_number_calculation()

        if io_condition(timestamp):
            perform_io_operations()

        if memory_intensive_condition(timestamp):
            perform_cpu_memory_intensive_task()

        if all_tasks_condition(timestamp):
            

            # Start the threads
            if not cpu_thread.is_alive():
                print('starter CPU task')
                cpu_thread = threading.Thread(target=perform_prime_number_calculation)
                cpu_thread.start()
            if not io_thread.is_alive():
                print('starter IO')
                io_thread = threading.Thread(target=perform_io_operations)
                io_thread.start()
            if not memory_thread.is_alive():
                print('MEM')
                memory_thread = threading.Thread(target=perform_cpu_memory_intensive_task)
                memory_thread.start()

            # Wait for all threads to complete
            #cpu_thread.join()
            #io_thread.join()
            #memory_thread.join()

        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent

        cpu_usages.append(cpu_usage)
        memory_usages.append(memory_usage)
        timestamps.append(timestamp - start_time)

        time.sleep(0.1)

    print("Stability test completed.")

    plot_stability(timestamps, cpu_usages, memory_usages, duration)

    
if __name__ == "__main__":
    stability_test()
