import unittest
from hrdc.usage import *
from hrdc.descriptor.test import descriptor_expected
from hrdc.descriptor import *

class TestBasicDescriptors(unittest.TestCase):
    def test_battery(self):
        battery = Collection(Collection.Application, consumer.ConsumerControl,
                             Collection(Collection.Logical, desktop.Keyboard,
                                        Value(Value.Input, device.BatteryStrength, 8,
                                              logicalMin = 0, logicalMax = 100)
                                        )
                             )

        descriptor_expected(self, battery, """
     0x05, 0x0c,                    // UsagePage (consumer)
     0x09, 0x01,                    // Usage (ConsumerControl)
     0xa1, 0x01,                    // Collection (Application)
     0x05, 0x01,                    //     UsagePage (desktop)
     0x09, 0x06,                    //     Usage (Keyboard)
     0xa1, 0x02,                    //     Collection (Logical)
     0x15, 0x00,                    //         LogicalMinimum (0)
     0x25, 0x64,                    //         LogicalMaximum (100)
     0x75, 0x08,                    //         ReportSize (8)
     0x95, 0x01,                    //         ReportCount (1)
     0x05, 0x06,                    //         UsagePage (device)
     0x09, 0x20,                    //         Usage (BatteryStrength)
     0x81, 0x02,                    //         Input (Variable)
     0xc0,                          //     EndCollection
     0xc0,                          // EndCollection
""")

    def test_keyboard(self):
        bit_in = lambda x: Value(Value.Input, x, 1,
                                 logicalMin = 0, logicalMax = 1)

        bit_out = lambda x: Value(Value.Output, x, 1,
                                  logicalMin = 0, logicalMax = 1)

        key_range = lambda n: Value(Value.Input, usage = None, size = 8,
                                    namedArray = UsageRange(keyboard.NoEvent, keyboard.KeypadHexadecimal),
                                    logicalMin = 0, count = n)

        descriptor = Collection(Collection.Application, desktop.Keyboard,
                              bit_in(keyboard.LeftControl),
                              bit_in(keyboard.LeftShift),
                              bit_in(keyboard.LeftAlt),
                              bit_in(keyboard.LeftGui),
                              bit_in(keyboard.RightControl),
                              bit_in(keyboard.RightShift),
                              bit_in(keyboard.RightAlt),
                              bit_in(keyboard.RightGui),

                              key_range(6),

                              bit_out(led.NumLock),
                              bit_out(led.CapsLock),
                              bit_out(led.ScrollLock),
                              )

        descriptor_expected(self, descriptor, """
     0x05, 0x01,                    // UsagePage (desktop)
     0x09, 0x06,                    // Usage (Keyboard)
     0xa1, 0x01,                    // Collection (Application)
     0x15, 0x00,                    //     LogicalMinimum (0)
     0x25, 0x01,                    //     LogicalMaximum (1)
     0x75, 0x01,                    //     ReportSize (1)
     0x95, 0x08,                    //     ReportCount (8)
     0x05, 0x07,                    //     UsagePage (keyboard)
     0x19, 0xe0,                    //     UsageMinimum (LeftControl)
     0x29, 0xe7,                    //     UsageMaximum (RightGui)
     0x81, 0x02,                    //     Input (Variable)
     0x26, 0xdd, 0x00,              //     LogicalMaximum (221)
     0x75, 0x08,                    //     ReportSize (8)
     0x95, 0x06,                    //     ReportCount (6)
     0x19, 0x00,                    //     UsageMinimum (NoEvent)
     0x29, 0xdd,                    //     UsageMaximum (KeypadHexadecimal)
     0x81, 0x00,                    //     Input
     0x25, 0x01,                    //     LogicalMaximum (1)
     0x75, 0x01,                    //     ReportSize (1)
     0x95, 0x03,                    //     ReportCount (3)
     0x05, 0x08,                    //     UsagePage (led)
     0x19, 0x01,                    //     UsageMinimum (NumLock)
     0x29, 0x03,                    //     UsageMaximum (ScrollLock)
     0x91, 0x02,                    //     Output (Variable)
     0xc0,                          // EndCollection
""")

    def test_mouse(self):
        mouse = Collection(Collection.Application, desktop.Mouse,
                           Value(Value.Input, desktop.X, 8,
                                 flags = Value.Variable | Value.Relative,
                                 logicalMin = -127, logicalMax = 127),
                           Value(Value.Input, desktop.Y, 8,
                                 flags = Value.Variable | Value.Relative,
                                 logicalMin = -127, logicalMax = 127),
                           Value(Value.Input, button.Button(1), 1,
                                 logicalMin = 0, logicalMax = 1),
                           Value(Value.Input, button.Button(2), 1,
                                 logicalMin = 0, logicalMax = 1),
                           Value(Value.Input, button.Button(3), 1,
                                 logicalMin = 0, logicalMax = 1),
                           )

        descriptor_expected(self, mouse, """        
     0x05, 0x01,                    // UsagePage (desktop)
     0x09, 0x02,                    // Usage (Mouse)
     0xa1, 0x01,                    // Collection (Application)
     0x15, 0x81,                    //     LogicalMinimum (-127)
     0x25, 0x7f,                    //     LogicalMaximum (127)
     0x75, 0x08,                    //     ReportSize (8)
     0x95, 0x02,                    //     ReportCount (2)
     0x09, 0x30,                    //     Usage (X)
     0x09, 0x31,                    //     Usage (Y)
     0x81, 0x06,                    //     Input (Variable|Relative)
     0x15, 0x00,                    //     LogicalMinimum (0)
     0x25, 0x01,                    //     LogicalMaximum (1)
     0x75, 0x01,                    //     ReportSize (1)
     0x95, 0x03,                    //     ReportCount (3)
     0x05, 0x09,                    //     UsagePage (button)
     0x19, 0x01,                    //     UsageMinimum (Button(1))
     0x29, 0x03,                    //     UsageMaximum (Button(3))
     0x81, 0x02,                    //     Input (Variable)
     0xc0,                          // EndCollection
""")
