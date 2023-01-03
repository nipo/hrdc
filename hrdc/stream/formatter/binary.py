from .base import Formatter

class Binary(Formatter):
    def __init__(self, output):
        import sys
        if output == sys.stdout and hasattr(output, "buffer"):
            self.output = output.buffer
        else:
            self.output = output

    def append(self, i):
        self.output.write(i.bytes())

    def close(self):
        pass
