from base import Formatter

class Binary(Formatter):
    def __init__(self, output):
        self.output = output

    def append(self, i):
        self.output.write(i.bytes())
