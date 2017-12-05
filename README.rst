================================
 HID Report Descriptor Compiler
================================

This project handles Human Interface Devices (HID_) Report
Descriptors.

This is a python library with associated tools to manipulate Report
Descriptors.

.. contents::

Presentation
============

Usually, report descriptors are authored in a source form directly.
Some_ tools_ exist, but they all concentrate on translating
representation of a descriptor, keeping it at the abstraction
level from Specification.

This project introduces a language for the semantic abstraction level
described in the spec, i.e. using Collection, Values and Reports as
first-class objects, not decomposed as Items.

Moreover, HID uses a lot of symbolic constants for Usage, Item types,
Data types, etc.  This should be transparent to the Report Descriptor
author.

Abstraction levels
==================

Two abstraction levels are handled by this library:

- the usual abstraction level from the HID specification. Various
  encoding are handled:

  - Binary data,

  - Hex blob,

  - C code with pretty comments.
  
- High-level descriptor: this is an abstract representation with
  Reports, Values, Collections, etc.

Compiler, converters
====================

Conversion between all these abstractions and encodings is supported
through:

- A generic HID Report Descriptor encoding converter,

- A Report Descriptor decompiler to get back to abstract
  representation,

- A report descriptor optimizing compiler.

Goal
====

If you are still reading, you probably know how to interpret this:

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
  0x81, 0x04,                    //     Input (Relative)
  0x15, 0x00,                    //     LogicalMinimum (0)
  0x25, 0x01,                    //     LogicalMaximum (1)
  0x75, 0x01,                    //     ReportSize (1)
  0x95, 0x03,                    //     ReportCount (3)
  0x05, 0x09,                    //     UsagePage (button)
  0x19, 0x01,                    //     UsageMinimum (Button(1))
  0x29, 0x03,                    //     UsageMaximum (Button(3))
  0x81, 0x02,                    //     Input (Variable)
  0xc0,                          // EndCollection

The whole purpose of this project is to stop editing this kind of
source code to concentrate on this:

.. code:: python

  descriptor = Collection(Collection.Application, desktop.Mouse,
      Value(Value.Input, desktop.X, 8, flags = Value.Relative, logicalMin = -127, logicalMax = 127),
      Value(Value.Input, desktop.Y, 8, flags = Value.Relative, logicalMin = -127, logicalMax = 127),
      Value(Value.Input, button.Button(1), 1, logicalMin = 0, logicalMax = 1),
      Value(Value.Input, button.Button(2), 1, logicalMin = 0, logicalMax = 1),
      Value(Value.Input, button.Button(3), 1, logicalMin = 0, logicalMax = 1),
  )

\... and let the computer take care of Global Items, Logical ranges,
Physical ranges, Units, etc.

More information
================

See documentation_ for more information about Usage_, `Descriptor
language`_ and rationale_.

See examples_.

License
=======

MIT

.. _HID: http://www.usb.org/developers/hidpage/
.. _some: https://github.com/DIGImend/hidrd/
.. _tools: http://www.usb.org/developers/tools/
.. _documentation: doc/index.rst
.. _usage: doc/usage.rst
.. _descriptor language: doc/descriptor.rst
.. _rationale: doc/why.rst
.. _examples: examples/
