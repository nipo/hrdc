import unittest
from hrdc.stream import item

class TestItemEncoding(unittest.TestCase):

    def test_signedness(self):
        self.assertEqual(item.Usage(6).bytes(), b'\x09\x06')
        self.assertEqual(item.Usage(0xff).bytes(), b'\x09\xff')
        self.assertEqual(item.Usage(0xffff).bytes(), b'\x0a\xff\xff')
        self.assertEqual(item.Usage(0x8000).bytes(), b'\x0a\x00\x80')

        self.assertEqual(item.LogicalMinimum(0).bytes(), b'\x15\x00')
        self.assertEqual(item.LogicalMinimum(6).bytes(), b'\x15\x06')
        self.assertEqual(item.LogicalMinimum(-5).bytes(), b'\x15\xfb')
        self.assertEqual(item.LogicalMinimum(0xffff).bytes(), b'\x17\xff\xff\x00\x00')
        self.assertEqual(item.LogicalMinimum(-32768).bytes(), b'\x16\x00\x80')
        self.assertEqual(item.LogicalMinimum(32767).bytes(), b'\x16\xff\x7f')
        self.assertEqual(item.LogicalMinimum(32768).bytes(), b'\x17\x00\x80\x00\x00')

    def test_zero_bits(self):
        self.assertEqual(item.EndCollection().bytes(), b'\xc0')

    def test_data_items(self):
        self.assertEqual(item.Input(item.Input.Variable).bytes(), b'\x81\x02')
        self.assertEqual(item.Output(item.Input.Variable).bytes(), b'\x91\x02')
        self.assertEqual(item.Feature(item.Input.Variable).bytes(), b'\xb1\x02')
