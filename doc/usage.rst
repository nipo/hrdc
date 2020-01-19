=======
 Usage
=======

For the examples here, we'll use a basic Mouse report descriptor.
This example descriptor will contain two relative axes (X and Y) and
Three buttons.

.. contents::

Input / Output Formats
======================

There are 2 main formats:

- HID Report descriptor (a stream of items) a.k.a. `low level`, this
  is the set of constructs defined in HID spec;
- HID Descriptor (a tree of Collections and Values) a.k.a. `high
  level` this is a custom language for `hrdc`, see `descriptor language`_.

Low level stream of item may be represented in three forms:

- Binary (this is how a device puts it on the wire),
- Hex (this is binary for humans, also outputted by Linux debugfs for
  HID devices),
- Code (a C array of byte values with comments in a textual form).

Library can parse and generate those three formats.

High-level descriptor format actually is a Python script calling
relevant library classes and functions, see `descriptor language`_.

Entry points
============

Low-level HID Report Descriptor converter
-----------------------------------------

Low-level HID report descriptor stream can be converted from one
representation to another with `hrdc.converter` entry point.  You may
invoke it with `python3 -m`:

.. code:: bash

  $ python3 -m hrdc.converter -h
  usage: converter.py [-h] [-i NAME] [-o NAME] [-O] [input] [output]
  
  Convert a HID report descriptor
  
  positional arguments:
    input                 Input file name
    output                Output file name
  
  optional arguments:
    -h, --help            show this help message and exit
    -i NAME, --input-format NAME
                          Input parser name
    -o NAME, --output-format NAME
                          Output formatter name
    -O, --optimize        Optimize stream

Optionnally, converter may optimize stream, see `optimization`_.

All files default to stdin / stdout.

For instance, let's say we have the following descriptor blob in its
hexadecimal format in `mouse.hex`:

.. code::

  05 01 09 02 a1 01 15 81 25 7f 75 08 95 02 09 30 09 31 81 06 15 00 25
  01 75 01 95 03 05 09 19 01 29 03 81 02 c0

It may be converted to C code with the following command line:

.. code:: bash

  $ python3 -m hrdc.converter -i hex -o code mouse.hex

which will output:

.. code:: c

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

Low-level converter extracts the source format to a stream of Items
with attached values.  It does not extract any semantic information.
The only constraint is to have balanced `Collection` and `End
Collection` items so that the pretty printer can indent correctly.

Because items are parsed and serialized back, the actual output may
not be the exact input.  For instance the following input stream:

.. code::

   0x26, 0x01, 0x00,                  // LogicalMaximum (1)

is outputted as:

.. code::

   0x25, 0x01,                        // LogicalMaximum (1)

There is no semantic validation / extraction.

Low-level to high-level descriptor decompiler
---------------------------------------------

This tool is invoked through `python3 -m hrdc.descriptor.extractor`.
The output file is a Python script containing a high-level
representation of the report descriptor.

.. code:: bash

  $ python3 -m hrdc.descriptor.extractor -h
  usage: extractor.py [-h] [-i NAME] [input] [output]
  
  Decompile a HID report descriptor
  
  positional arguments:
    input                 Input file name
    output                Output file name
  
  optional arguments:
    -h, --help            show this help message and exit
    -i NAME, --input-format NAME
                          Input parser name

All files default to stdin / stdout.

The same mouse descriptor as above would be extracted with:

.. code:: bash

  $ python3 -m hrdc.descriptor.extractor -i hex mouse.hex mouse.py

In turn, this file can be used as a python script.  `compile_main`
directive at end of file will handle a command line, see `descriptor
language`_.

High-level Descriptor Compiler
------------------------------

High level descriptor compiler takes input from a Python script using
the `hrdc` library components to model a tree of:

- Collections,
- Reports,
- Values.

Values are data items in HID terminology.  Values can be:

- Single absolute/relative items,
- Named Arrays (surrounding logical collection is implicit),
- Data arrays,
- Padding.

A HID mouse device descriptor source code could be:

.. code:: python

  from hrdc.usage import *
  from hrdc.descriptor import *
  
  descriptor = Collection(Collection.Application, desktop.Mouse,
      Value(Value.Input, desktop.X, 8, flags = Value.Variable | Value.Relative, logicalMin = -127, logicalMax = 127),
      Value(Value.Input, desktop.Y, 8, flags = Value.Variable | Value.Relative, logicalMin = -127, logicalMax = 127),
      Value(Value.Input, button.Button(1), 1, logicalMin = 0, logicalMax = 1),
      Value(Value.Input, button.Button(2), 1, logicalMin = 0, logicalMax = 1),
      Value(Value.Input, button.Button(3), 1, logicalMin = 0, logicalMax = 1),
  )
  
  if __name__ == "__main__":
      compile_main(descriptor)

Execution of this script will handle a command-line and allow
generation of an output HID report descriptor item stream.

.. code:: bash

  $ python3 mouse.py -h
  usage: mouse.py [-h] [-o NAME] [-N] [output]
  
  Compile a HID report descriptor
  
  positional arguments:
    output                Output file name
  
  optional arguments:
    -h, --help            show this help message and exit
    -o NAME, --output-format NAME
                          Output formatter name
    -N, --no-optimize     Dont optimize output stream

Please note default behavior is to optimize output stream, contrary to
the HID Report Descriptor converter above, because non-optimized
stream generated by descriptor serializer is mostly useless.

Here is an example of non-optimized report:

.. code:: bash

  $ python3 mouse.py -N -o code
       0x0b, 0x02, 0x00, 0x01, 0x00,  // Usage (desktop.Mouse)
       0xa1, 0x01,                    // Collection (Application)
       0x0b, 0x30, 0x00, 0x01, 0x00,  //     Usage (desktop.X)
       0x35, 0x00,                    //     PhysicalMinimum (0)
       0x45, 0x00,                    //     PhysicalMaximum (0)
       0x15, 0x81,                    //     LogicalMinimum (-127)
       0x25, 0x7f,                    //     LogicalMaximum (127)
       0x65, 0x00,                    //     Unit (0)
       0x55, 0x00,                    //     UnitExponent (0)
       0x95, 0x01,                    //     ReportCount (1)
       0x75, 0x08,                    //     ReportSize (8)
       0x81, 0x06,                    //     Input (Variable|Relative)
       0x0b, 0x31, 0x00, 0x01, 0x00,  //     Usage (desktop.Y)
       0x35, 0x00,                    //     PhysicalMinimum (0)
       0x45, 0x00,                    //     PhysicalMaximum (0)
       0x15, 0x81,                    //     LogicalMinimum (-127)
       0x25, 0x7f,                    //     LogicalMaximum (127)
       0x65, 0x00,                    //     Unit (0)
       0x55, 0x00,                    //     UnitExponent (0)
       0x95, 0x01,                    //     ReportCount (1)
       0x75, 0x08,                    //     ReportSize (8)
       0x81, 0x06,                    //     Input (Variable|Relative)
       0x0b, 0x01, 0x00, 0x09, 0x00,  //     Usage (button.Button(1))
       0x35, 0x00,                    //     PhysicalMinimum (0)
       0x45, 0x00,                    //     PhysicalMaximum (0)
       0x15, 0x00,                    //     LogicalMinimum (0)
       0x25, 0x01,                    //     LogicalMaximum (1)
       0x65, 0x00,                    //     Unit (0)
       0x55, 0x00,                    //     UnitExponent (0)
       0x95, 0x01,                    //     ReportCount (1)
       0x75, 0x01,                    //     ReportSize (1)
       0x81, 0x02,                    //     Input (Variable)
       0x0b, 0x02, 0x00, 0x09, 0x00,  //     Usage (button.Button(2))
       0x35, 0x00,                    //     PhysicalMinimum (0)
       0x45, 0x00,                    //     PhysicalMaximum (0)
       0x15, 0x00,                    //     LogicalMinimum (0)
       0x25, 0x01,                    //     LogicalMaximum (1)
       0x65, 0x00,                    //     Unit (0)
       0x55, 0x00,                    //     UnitExponent (0)
       0x95, 0x01,                    //     ReportCount (1)
       0x75, 0x01,                    //     ReportSize (1)
       0x81, 0x02,                    //     Input (Variable)
       0x0b, 0x03, 0x00, 0x09, 0x00,  //     Usage (button.Button(3))
       0x35, 0x00,                    //     PhysicalMinimum (0)
       0x45, 0x00,                    //     PhysicalMaximum (0)
       0x15, 0x00,                    //     LogicalMinimum (0)
       0x25, 0x01,                    //     LogicalMaximum (1)
       0x65, 0x00,                    //     Unit (0)
       0x55, 0x00,                    //     UnitExponent (0)
       0x95, 0x01,                    //     ReportCount (1)
       0x75, 0x01,                    //     ReportSize (1)
       0x81, 0x02,                    //     Input (Variable)
       0xc0,                          // EndCollection

Next steps:

- `descriptor language`_,
- `optimization`_.

.. _`optimization`: optimizations.rst
.. _`descriptor language`: descriptor.rst
