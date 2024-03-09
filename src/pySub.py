import threading
import queue
import time

class Topic:
    def __init__(self):
        self.subscribers = set()
        
    def set_final(self, final):
        self.final = final

    def subscribe(self, subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def publish(self, message):
        for subscriber in self.subscribers:
            subscriber.queue.put(message)

    def stop_all_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.queue.put("exit")
            subscriber.join()

class Subscriber(threading.Thread):
    def __init__(self, name, publisher):
        super().__init__(name=name)
        self.publisher = publisher
        self.queue = queue.Queue()

    def run(self):
        while True:
            message = self.queue.get()
            if message == "exit":
                break
            print(f"{self.name} received: {message}")

    def set_run(self, run):
        self.run = run