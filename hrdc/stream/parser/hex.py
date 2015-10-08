from base import Parser
import re

class Hex(Parser):
    def read(self, *args):
        contents = self.input.read(*args)
        blob = ''.join(map(lambda x:chr(int(x, 16)),
                           re.findall(r"\b(?:0x)?[0-9A-Fa-f]{2}\b", contents)))
        self.blobParse(blob)
            
