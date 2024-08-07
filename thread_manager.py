import threading
import time
import random
from cpu_monitor import CPUMonitor

class WorkerThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True:
            # Simulate work by sleeping for a random time
            time.sleep(random.uniform(0.1, 0.5))
            # Simulate high CPU usage
            if random.random() > 0.8:
                for _ in range(10000000):
                    pass

def main():
    threads = []
    num_threads = 5
    cpu_monitor = CPUMonitor(threshold=10.0, interval=1)

    # Create and start threads
    for i in range(num_threads):
        thread = WorkerThread(name=f"Thread-{i+1}")
        thread.start()
        threads.append(thread)
        cpu_monitor.register_thread(thread)

    cpu_monitor.start()

    # Keep the main program running to monitor threads
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping all threads...")
        cpu_monitor.stop()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
