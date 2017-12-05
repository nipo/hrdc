from .base import Parser
import re

class Code(Parser):
    def read(self, *args):
        contents = ""
        for line in self.input.read(*args).split("\n"):
            contents += line.split("//", 1)[0] + " "
        contents = re.sub(r"/\*.*?\*/", "", contents)
        contents = re.sub(r"\s+", "", contents)
        blob = bytes(int(x, 16) for x in contents.split(",") if x)
        self.blobParse(blob)
            
