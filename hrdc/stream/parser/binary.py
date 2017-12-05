from .base import Parser

class Binary(Parser):
    def __init__(self, input, output):
        import sys

        if input == sys.stdin and hasattr(input, "buffer"):
            input = input.buffer

        Parser.__init__(self, input, output)

    def read(self, *args):
        blob = self.input.read(*args)
        self.blobParse(blob)
            
