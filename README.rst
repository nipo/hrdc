================================
 HID Report Descriptor Compiler
================================

Presentation
============

This toolset handles Human Interface Devices (HID_) Report
Descriptors.

Two representation levels are handled:

- Low-level stream of /Item/\s: this is the specification defintion
  abstraction level,
- High-level descriptor: this is an abstract representation with
  Reports, Values, Collections, etc.

This project contains all tools to convert between various formats, i.e.:

- Compile to a report descriptor blob from a high-level descriptor,
- Extract high-level descriptor from descriptor blob (a sort of
  descriptor decompiler),
- Optimize a report descriptor.

Moreover, most Usage Pages are resolved in a symbolic format.

Converters
==========

Parser
------

Let's say we have a report descriptor blob in hex form::

  $ cat report.hex
  05 01 09 02 a1 01 15 81 25 7f 75 08 95 02 09 30 09 31 81 04 15 00 25
  01 75 01 95 03 05 09 19 01 29 03 81 02 c0

We can parse it to extract its code representation::

  $ python -m hrdc.converter -i hex -o code report.hex
       0x05, 0x01,                    // UsagePage (GenericDesktop)
       0x09, 0x02,                    // Usage (Mouse)
       0xa1, 0x01,                    // Collection (Application)
       0x15, 0x81,                    //     LogicalMinimum (-127)
       0x25, 0x7f,                    //     LogicalMaximum (127)
       0x75, 0x08,                    //     ReportSize (8)
       0x95, 0x02,                    //     ReportCount (2)
       0x09, 0x30,                    //     Usage (X)
       0x09, 0x31,                    //     Usage (Y)
       0x81, 0x04,                    //     Input (Relative)
       0x15, 0x00,                    //     LogicalMinimum (0)
       0x25, 0x01,                    //     LogicalMaximum (1)
       0x75, 0x01,                    //     ReportSize (1)
       0x95, 0x03,                    //     ReportCount (3)
       0x05, 0x09,                    //     UsagePage (Button)
       0x19, 0x01,                    //     UsageMinimum (Button(1))
       0x29, 0x03,                    //     UsageMaximum (Button(3))
       0x81, 0x02,                    //     Input (Variable)
       0xc0,                          // EndCollection

Decompiler
----------

Now, we can also parse this blob and output a high-level descripor
source code::

  $ python -m hrdc.descriptor.extractor -i hex report.hex 
  from hrdc.usage import *
  from hrdc.descriptor import *
  
  descriptor = TopLevel(
      Report(0,
          Collection(Collection.Application, desktop.Mouse,
              Value(Value.Input, desktop.X, 8, flags = Value.Relative, logicalMin = -127, logicalMax = 127),
              Value(Value.Input, desktop.Y, 8, flags = Value.Relative, logicalMin = -127, logicalMax = 127),
              Value(Value.Input, button.Button(1), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(2), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(3), 1, logicalMin = 0, logicalMax = 1),
          ),
      ),
  )
  
  if __name__ == "__main__":
      compile_main(descriptor)

Compiler
--------

As it turns out, extracted descriptor is actually a valid python
script using the library to compile back to a descriptor blob.  Lets
write it to a file::

  $ python -m hrdc.descriptor.extractor -i hex report.hex report.py

And compile it::

  $ python report.py -o code
  [... the same report source code outputs]

Optimizer
=========

When spilling report descriptor from high-level representation,
compiler is dump: It repeats all items for all data items, and never
uses Usage Page Items.

Library contains a report descriptor optimizer that respects all
aspects of local, global and main items, resets units when relevant,
etc.  It is used by default (when not setting "-N" on command line)::

  $ python report.py -N -o hex | wc -w
       123
  $ python report.py -o hex | wc -w
        37
