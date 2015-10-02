__author__ = 'ginezf'
import threading


class Thread:

    def __init__(self, thread_function):
        self.t = None
        self.thread_function = thread_function
        pass

    def run(self):
        return self.thread_function()
        pass

    def start(self):
        self.t = threading.Thread(target=self.run)

    def join(self):
        self.t.join()
