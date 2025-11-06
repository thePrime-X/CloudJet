import threading
import time
import multiprocessing

# Duration to run the stress test (in seconds)
DURATION = 315  # 5 minutes

# Function to keep CPU busy
def cpu_stress():
    end_time = time.time() + DURATION
    while time.time() < end_time:
        x = 0
        for i in range(1000000):
            x += i*i

# Get the number of CPU cores
num_cores = multiprocessing.cpu_count()

# Create a thread for each core
threads = []
for _ in range(num_cores):
    t = threading.Thread(target=cpu_stress)
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

print("CPU stress test complete!")
