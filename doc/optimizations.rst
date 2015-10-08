=====================================
 HID Report Descriptor Optimizations
=====================================

When serializing HID report descriptors, `hrdc` can optimize them to
get the canonical report descriptor, avoiding any redundancy of items.

Various optimization passes are implemented in the library.  All
together, they produce a decent report descriptor data stream.

Here is an overview of each pass.

.. contents::

Global merging
==============

In a HID report descriptor, Globals are, as you may think, global.
This means their value is never reset by another item.

This pass remove duplicates items that set a global item to a value it
already has.

Main merging
============

Main items are Collection or Data items.  This pass merges Data items
that have the same characteristics.  For instance, defining three
buttons could explicitly be declared as:

.. code:: c

  0x15, 0x00,                    //     LogicalMinimum (0)
  0x25, 0x01,                    //     LogicalMaximum (1)
  0x75, 0x01,                    //     ReportSize (1)
  0x95, 0x01,                    //     ReportCount (1)
  0x05, 0x09,                    //     UsagePage (button)
  0x09, 0x01,                    //     Usage (Button(1))
  0x81, 0x02,                    //     Input (Variable)
  0x09, 0x02,                    //     Usage (Button(2))
  0x81, 0x02,                    //     Input (Variable)
  0x09, 0x03,                    //     Usage (Button(3))
  0x81, 0x02,                    //     Input (Variable)

This pass merges the three declarations to one with an ajusted
ReportCount:

.. code:: c

  0x15, 0x00,                    //     LogicalMinimum (0)
  0x25, 0x01,                    //     LogicalMaximum (1)
  0x75, 0x01,                    //     ReportSize (1)
  0x95, 0x03,                    //     ReportCount (3)
  0x05, 0x09,                    //     UsagePage (button)
  0x09, 0x01,                    //     Usage (Button(1))
  0x09, 0x02,                    //     Usage (Button(2))
  0x09, 0x03,                    //     Usage (Button(3))
  0x81, 0x02,                    //     Input (Variable)

Note: `Range merging`_ will optimize this further.

Physical Merging
================

Physical Minimum and Physical Maximum are globals, but they also have
an interesting side effect: if they are both set to 0, they actually
take values from Logical range.

This pass resets Physical range for all cases where it matches Logical
range, in the hope there will be no need to redeclare it on next item.

Range merging
=============

Usage, String Index and Designator Index are local items that can
either be declared one-by-one, or declared as ranges.

This pass is a generic pass that can merge multiple simple local items
to their range counterpart.

For instance, this descriptor:

.. code:: c

  0x15, 0x00,                    //     LogicalMinimum (0)
  0x25, 0x01,                    //     LogicalMaximum (1)
  0x75, 0x01,                    //     ReportSize (1)
  0x95, 0x03,                    //     ReportCount (3)
  0x05, 0x09,                    //     UsagePage (button)
  0x09, 0x01,                    //     Usage (Button(1))
  0x09, 0x02,                    //     Usage (Button(2))
  0x09, 0x03,                    //     Usage (Button(3))
  0x81, 0x02,                    //     Input (Variable)

would be optimized as:

.. code:: c

  0x15, 0x00,                    //     LogicalMinimum (0)
  0x25, 0x01,                    //     LogicalMaximum (1)
  0x75, 0x01,                    //     ReportSize (1)
  0x95, 0x03,                    //     ReportCount (3)
  0x05, 0x09,                    //     UsagePage (button)
  0x19, 0x01,                    //     Usage Minimum (Button(1))
  0x29, 0x03,                    //     Usage Maximum (Button(3))
  0x81, 0x02,                    //     Input (Variable)

Usage Page
==========

This pass takes 32-bit Usage items and splits them as two items, one
Usage Page item and one Usage item.  Usage page will only be reset if
needed.

Designator Uniq
===============

This pass merges Designator items that have the same value as
previous, avoiding redundancy.  This is mostly useful for default
situation where no designator is set at all, but where descriptor
compiler still outputs a `Designator(0)` item.
