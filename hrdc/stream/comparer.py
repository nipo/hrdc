import re
from . import stream
from .formatter.binary import Binary
from .parser.code import Code

class ExpectedStream(stream.Stream):
    def __init__(self, test_case, expected_code):
        self.test_case = test_case

        contents = ""
        for line in expected_code.split("\n"):
            contents += line.split("//", 1)[0] + " "
        contents = re.sub(r"/\*.*?\*/", "", contents)
        contents = re.sub(r"\s+", "", contents)
        self.expected = bytes(int(x, 16) for x in contents.split(",") if x)
        self.point = 0

    def append(self, item):
        part = item.bytes()
        expected = self.expected[self.point : self.point + len(part)]
        self.test_case.assertEqual(expected, part)
        self.point += len(part)

    def close(self):
        self.test_case.assertEqual(self.point, len(self.expected))
