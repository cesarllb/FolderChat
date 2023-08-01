# import time module, Observer, FileSystemEventHandler
import time
import threading
from queue import Queue
from folderchat.logging import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

		
class WatchdogThread(threading.Thread):

    def __init__(self, data_source:str, event_queue: Queue):
        threading.Thread.__init__(self)
        self.watchDirectory = data_source
        self.daemon = True

    def run(self):
        observer = Observer()
        observer.schedule(Handler(), self.watchDirectory, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            observer.stop()
            logger.info("Watchdog has stopped")

        observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, event_queue: Queue):
        super().__init__()
        self.event_queue = event_queue

    @staticmethod
    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            logger.info("Watchdog received created event - % s." % event.src_path)
            self.event_queue.put(event)
        elif event.event_type == 'modified':
            logger.info("Watchdog received modified event - % s." % event.src_path)
            self.event_queue.put(event)