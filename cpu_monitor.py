import psutil
import time
import threading

class CPUMonitor:
    def __init__(self, threshold, interval):
        self.threshold = threshold
        self.interval = interval
        self.threads = []
        self.monitoring = False

    def register_thread(self, thread):
        self.threads.append(thread)

    def start(self):
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor)
        self.monitor_thread.start()

    def stop(self):
        self.monitoring = False
        self.monitor_thread.join()

    def monitor(self):
        while self.monitoring:
            for thread in self.threads:
                try:
                    thread_cpu = psutil.Process(thread.ident).cpu_percent(interval=None)
                    if thread_cpu > self.threshold:
                        print(f"Terminating {thread.name} due to high CPU usage: {thread_cpu}%")
                        thread.do_run = False
                        thread.join()
                except psutil.NoSuchProcess:
                    continue
            time.sleep(self.interval)
