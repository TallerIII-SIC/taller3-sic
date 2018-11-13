import time

class Timer(object):
    def __init__(self):
        self.st = 0

    def start(self):
        self.st = time.time()

    def end(self, msg):
        end = time.time()
        print(msg.format(end - self.st))
