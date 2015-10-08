import unittest
from ..stream import item

class TestItemEncoding(unittest.TestCase):

    def test_signedness(self):
        self.assertEqual(item.Usage(6).bytes(), '\x09\x06')
        self.assertEqual(item.Usage(0xff).bytes(), '\x09\xff')
        self.assertEqual(item.Usage(0xffff).bytes(), '\x0a\xff\xff')
        self.assertEqual(item.Usage(0x8000).bytes(), '\x0a\x00\x80')

        self.assertEqual(item.LogicalMinimum(0).bytes(), '\x15\x00')
        self.assertEqual(item.LogicalMinimum(6).bytes(), '\x15\x06')
        self.assertEqual(item.LogicalMinimum(-5).bytes(), '\x15\xfb')
        self.assertEqual(item.LogicalMinimum(0xffff).bytes(), '\x17\xff\xff\x00\x00')
        self.assertEqual(item.LogicalMinimum(-32768).bytes(), '\x16\x00\x80')
        self.assertEqual(item.LogicalMinimum(32767).bytes(), '\x16\xff\x7f')
        self.assertEqual(item.LogicalMinimum(32768).bytes(), '\x17\x00\x80\x00\x00')

    def test_zero_bits(self):
        self.assertEqual(item.EndCollection().bytes(), '\xc0')

    def test_data_items(self):
        self.assertEqual(item.Input(item.Input.Variable).bytes(), '\x81\x02')
        self.assertEqual(item.Output(item.Input.Variable).bytes(), '\x91\x02')
        self.assertEqual(item.Feature(item.Input.Variable).bytes(), '\xb1\x02')

if __name__ == '__main__':
    unittest.main()
    
