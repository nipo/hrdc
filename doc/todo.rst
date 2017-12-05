========
 TO-DOs
========

Using this library as starting point, we may:

- provide high-level building blocks for usual constructs.

- create a visitor for a descriptor tree that outputs C structures
  definitions matching the defined reports.

- implement passes to improve optimization of report descriptors.
  Some usual optimization directions involve reordering values to
  group them by usage page, or reorder usages to be able to use
  ranges.  As this changes semantics of descriptors, this should
  probably yield warnings rather than do modifications directly.

- parse / generate foreign tools native data formats (`HID Descriptor
  Tool` is one of them).
