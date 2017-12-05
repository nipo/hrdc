from .base import Parser
import re

class Hex(Parser):
    def read(self, *args):
        contents = self.input.read(*args)
        blob = bytes(int(x, 16) for x in re.findall(r"\b(?:0x)?[0-9A-Fa-f]{2}\b", contents))
        self.blobParse(blob)
            
