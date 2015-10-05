__author__ = 'ginezf'
from threading import *


class Threadable:

    def __init__(self, thread_function):
        self.t = None
        self.thread_function = thread_function
        pass

    def run(self):
        return self.thread_function()
        pass

    def start(self):
        self.t = Thread(target=self.run)

    def join(self):
        self.t.join()