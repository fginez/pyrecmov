__author__ = 'ginezf'
from threading import *


class Threadable:

    def __init__(self, thread_function):
        self.t = None
        self.thread_function = thread_function
        pass

    def run(self):
        print "Threadable::run - Starting thread function"
        return self.thread_function()
        pass

    def start(self):
        print "Starting thread"
        self.t = Thread(target=self.run)
        self.t.start()

    def join(self):
        self.t.join()
