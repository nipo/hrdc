import unittest
from hrdc.usage import *
from hrdc.descriptor.test import descriptor_expected
from hrdc.descriptor import *

descriptor = Collection(Collection.Application, sensors.Environmental,
    Collection(Collection.Physical, sensors.Environmental,
        Report(1,
            Value(Value.Input, sensors.EnvironmentalHumidity, 16, logicalMin = 0, logicalMax = 1400),
            Value(Value.Input, sensors.EnvironmentalTemperature, 8, logicalMin = 0, logicalMax = 100, count = 2),
            Value(Value.Input, sensors.EnvironmentalAtmosphericPressure, 8, logicalMin = 0, logicalMax = 100),
        ),
    ),
)

class TestIssue7(unittest.TestCase):
    def test_item_merging(self):
        descriptor_expected(self, descriptor, """
     0x05, 0x20,                    // UsagePage (sensors)
     0x09, 0x30,                    // Usage (Environmental)
     0xa1, 0x01,                    // Collection (Application)
     0x09, 0x30,                    //     Usage (Environmental)
     0xa1, 0x00,                    //     Collection (Physical)
     0x85, 0x01,                    //         ReportID (1)
     0x15, 0x00,                    //         LogicalMinimum (0)
     0x26, 0x78, 0x05,              //         LogicalMaximum (1400)
     0x75, 0x10,                    //         ReportSize (16)
     0x95, 0x01,                    //         ReportCount (1)
     0x09, 0x32,                    //         Usage (EnvironmentalHumidity)
     0x81, 0x02,                    //         Input (Variable)
     0x25, 0x64,                    //         LogicalMaximum (100)
     0x75, 0x08,                    //         ReportSize (8)
     0x95, 0x02,                    //         ReportCount (2)
     0x09, 0x33,                    //         Usage (EnvironmentalTemperature)
     0x81, 0x02,                    //         Input (Variable)
     0x95, 0x01,                    //         ReportCount (1)
     0x09, 0x31,                    //         Usage (EnvironmentalAtmosphericPressure)
     0x81, 0x02,                    //         Input (Variable)
     0xc0,                          //     EndCollection
     0xc0,                          // EndCollection
""")

if __name__ == '__main__':
    compile_main(descriptor)
    
