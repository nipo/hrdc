from base import Formatter

class Hex(Formatter):
    def __init__(self, output):
        self.output = output

    def append(self, i):
        blob = " ".join(map(lambda x: "%02x" % ord(x), i.bytes()))
        self.output.write(blob + "\n")
