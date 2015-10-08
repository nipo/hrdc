from base import Parser

class Binary(Parser):
    def read(self, *args):
        blob = self.input.read(*args)
        self.blobParse(blob)
            
