from .base import Formatter

class Hex(Formatter):
    def __init__(self, output):
        self.output = output

    def append(self, i):
        blob = " ".join(["%02x" % x for x in i.bytes()])
        self.output.write(blob + "\n")

    def close(self):
        pass
