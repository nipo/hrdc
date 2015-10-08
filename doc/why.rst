==============================
 Why use a compiler for HID ?
==============================

HID is simple enough for a trained engineer to assume it can be
authored by hand.  This is wrong.  Unfortunately, HID is hard enough
for most bugs to be forgotten in a final product, and when a product
ships bug-free, most of the time, there is room for improvement.

.. contents::

HID is Error prone
==================

HID is error prone.  Because of mix of local and global items, some
parameters have to be reset between data items, others may not.
Moreover, some items (i.e. Physical range) have an implicit value that
depend on others if set to 0.

Some examples may be of some interest.

A sample gamepad
----------------

This report descriptor is a excerpt from an existing product.  It has
been extracted directly from device.  This is the first main
collection (there are others collections, irrelevant for the example).

Hex form:

.. code::

  05 01 09 05 A1 01 85 01 05 09 19 01 29 0F 15 00 25 01 95 0F 75 01 81
  02 75 01 95 01 81 03 05 01 09 39 15 01 25 08 35 00 46 3B 01 66 14 00
  75 04 95 01 81 42 75 04 95 01 81 03 05 01 09 01 A1 00 09 30 09 31 15
  00 26 FF FF 35 00 46 FF FF 95 02 75 10 81 02 C0 09 32 09 35 15 00 26
  FF FF 35 00 46 FF FF 95 02 75 10 81 02 05 02 09 C5 09 C4 15 00 26 FF
  FF 35 00 46 FF FF 95 02 75 10 81 02 C0

Corresponding code with textual form, from a `sibling tool`_:

.. code:: bash
  :number-lines:
  
  $ hidrd-convert -i hex -o code broken.hex
      0x05, 0x01,         /*  Usage Page (Desktop),               */
      0x09, 0x05,         /*  Usage (Gamepad),                    */
      0xA1, 0x01,         /*  Collection (Application),           */
      0x85, 0x01,         /*      Report ID (1),                  */
      0x05, 0x09,         /*      Usage Page (Button),            */
      0x19, 0x01,         /*      Usage Minimum (01h),            */
      0x29, 0x0F,         /*      Usage Maximum (0Fh),            */
      0x15, 0x00,         /*      Logical Minimum (0),            */
      0x25, 0x01,         /*      Logical Maximum (1),            */
      0x95, 0x0F,         /*      Report Count (15),              */
      0x75, 0x01,         /*      Report Size (1),                */
      0x81, 0x02,         /*      Input (Variable),               */
      0x75, 0x01,         /*      Report Size (1),                */
      0x95, 0x01,         /*      Report Count (1),               */
      0x81, 0x03,         /*      Input (Constant, Variable),     */
      0x05, 0x01,         /*      Usage Page (Desktop),           */
      0x09, 0x39,         /*      Usage (Hat Switch),             */
      0x15, 0x01,         /*      Logical Minimum (1),            */
      0x25, 0x08,         /*      Logical Maximum (8),            */
      0x35, 0x00,         /*      Physical Minimum (0),           */
      0x46, 0x3B, 0x01,   /*      Physical Maximum (315),         */
      0x66, 0x14, 0x00,   /*      Unit (Degrees),                 */
      0x75, 0x04,         /*      Report Size (4),                */
      0x95, 0x01,         /*      Report Count (1),               */
      0x81, 0x42,         /*      Input (Variable, Null State),   */
      0x75, 0x04,         /*      Report Size (4),                */
      0x95, 0x01,         /*      Report Count (1),               */
      0x81, 0x03,         /*      Input (Constant, Variable),     */
      0x05, 0x01,         /*      Usage Page (Desktop),           */
      0x09, 0x01,         /*      Usage (Pointer),                */
      0xA1, 0x00,         /*      Collection (Physical),          */
      0x09, 0x30,         /*          Usage (X),                  */
      0x09, 0x31,         /*          Usage (Y),                  */
      0x15, 0x00,         /*          Logical Minimum (0),        */
      0x26, 0xFF, 0xFF,   /*          Logical Maximum (-1),       */
      0x35, 0x00,         /*          Physical Minimum (0),       */
      0x46, 0xFF, 0xFF,   /*          Physical Maximum (-1),      */
      0x95, 0x02,         /*          Report Count (2),           */
      0x75, 0x10,         /*          Report Size (16),           */
      0x81, 0x02,         /*          Input (Variable),           */
      0xC0,               /*      End Collection,                 */
      0x09, 0x32,         /*      Usage (Z),                      */
      0x09, 0x35,         /*      Usage (Rz),                     */
      0x15, 0x00,         /*      Logical Minimum (0),            */
      0x26, 0xFF, 0xFF,   /*      Logical Maximum (-1),           */
      0x35, 0x00,         /*      Physical Minimum (0),           */
      0x46, 0xFF, 0xFF,   /*      Physical Maximum (-1),          */
      0x95, 0x02,         /*      Report Count (2),               */
      0x75, 0x10,         /*      Report Size (16),               */
      0x81, 0x02,         /*      Input (Variable),               */
      0x05, 0x02,         /*      Usage Page (Simulation),        */
      0x09, 0xC5,         /*      Usage (Brake),                  */
      0x09, 0xC4,         /*      Usage (Accelerator),            */
      0x15, 0x00,         /*      Logical Minimum (0),            */
      0x26, 0xFF, 0xFF,   /*      Logical Maximum (-1),           */
      0x35, 0x00,         /*      Physical Minimum (0),           */
      0x46, 0xFF, 0xFF,   /*      Physical Maximum (-1),          */
      0x95, 0x02,         /*      Report Count (2),               */
      0x75, 0x10,         /*      Report Size (16),               */
      0x81, 0x02,         /*      Input (Variable),               */
      0xC0                /*  End Collection                      */

This defines a gamepad, 15 buttons, a hat switch, two thumb sticks and
two analog triggers.

There are some broken constructs a compiler could do nothing about:

- line 43, the second thumb stick using Z and Rz as axis Usage codes
  instead of X and Y in another Physical Collection (see `HUT1_12v2`_,
  A.5, p. 132);

- line 53, analog triggers use specific usages even if nothing
  enforces using those two triggers for "Accelerator" and "Brake".
  Actually, specification explicitly says "Button" usages should be
  preferred over specific usages (see `HID1_11`_, 6.2.2.8, in
  footnote, p. 40).

There are other constructs where a compiler could have been useful:

- line 35 onwards, range for analog controls is broken, it goes from 0
  to -1.  Logical minimum and Logical maximum are signed, value is 16
  bits, maximum should have been defined with a 4-byte item (most HID
  parsers are tolerant about this one);

- finally, this descriptor is suboptimal.  It repeats physical bounds
  that are the same as logical ones.  Repeating them is not needed as
  physical range is meant to be the same as logical one when both
  physical minimum and physical maximum are 0 (see `HID1_11`_,
  6.2.2.7, p. 38).

But they are not the worst thing.  There is a blatant error.  With
extractor, it may become clearer:

.. code:: bash

  $ python -m hrdc.descriptor.extractor -i hex broken.hex

.. code:: python
  :number-lines:

  from hrdc.usage import *
  from hrdc.descriptor import *
  
  descriptor = TopLevel(
      Report(1,
          Collection(Collection.Application, desktop.Gamepad,
              Value(Value.Input, button.Button(1), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(2), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(3), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(4), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(5), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(6), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(7), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(8), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(9), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(10), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(11), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(12), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(13), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(14), 1, logicalMin = 0, logicalMax = 1),
              Value(Value.Input, button.Button(15), 1, logicalMin = 0, logicalMax = 1),
              Padding(Value.Input, 1),
              Value(Value.Input, desktop.HatSwitch, 4, flags = Value.Variable|Value.NullState, logicalMax = 8, physicalMin = 0, physicalMax = 315, unit = Unit.Degree),
              Padding(Value.Input, 4),
              Collection(Collection.Physical, desktop.Pointer,
                  Value(Value.Input, desktop.X, 16, logicalMin = 0, logicalMax = -1, unit = Unit.Degree),
                  Value(Value.Input, desktop.Y, 16, logicalMin = 0, logicalMax = -1, unit = Unit.Degree),
              ),
              Value(Value.Input, desktop.Z, 16, logicalMin = 0, logicalMax = -1, unit = Unit.Degree),
              Value(Value.Input, desktop.Rz, 16, logicalMin = 0, logicalMax = -1, unit = Unit.Degree),
              Value(Value.Input, simulation.Brake, 16, logicalMin = 0, logicalMax = -1, unit = Unit.Degree),
              Value(Value.Input, simulation.Accelerator, 16, logicalMin = 0, logicalMax = -1, unit = Unit.Degree),
          ),
      ),
  )
  
  if __name__ == "__main__":
      compile_main(descriptor)

After the Hat switch definition, line 23, all subsequent values have
Degree as unit. This is most probably not wanted.

Why did this happen ? Because Unit is a global item, but this may
easily be forgotten about.  A `Unit()` item should have reset the unit
somewhere after line 26 of descriptor above.

Another gamepad
---------------

Again, here is a binary descriptor from an actual device:

.. code::

  05 01 09 05 a1 01 05 01 09 01 a1 00 05 09 19 01 29 0c 15 00 25 01 75
  01 95 0c 81 02 75 08 95 01 81 01 05 01 09 39 25 07 35 00 46 0e 01 66
  40 00 75 04 81 42 09 30 09 31 15 80 25 7f 46 ff 00 66 00 00 75 08 95
  02 81 02 09 35 95 01 81 02 09 36 16 00 00 26 ff 00 81 02 09 bb 15 00
  26 ff 00 35 00 46 ff 00 75 08 95 04 91 02 c0 c0

Spec-annotated code:

.. code:: bash
  :number-lines:

  $ hidrd-convert -i hex -o code broken2.hex
      0x05, 0x01,         /*  Usage Page (Desktop),                   */
      0x09, 0x05,         /*  Usage (Gamepad),                        */
      0xA1, 0x01,         /*  Collection (Application),               */
      0x05, 0x01,         /*      Usage Page (Desktop),               */
      0x09, 0x01,         /*      Usage (Pointer),                    */
      0xA1, 0x00,         /*      Collection (Physical),              */
      0x05, 0x09,         /*          Usage Page (Button),            */
      0x19, 0x01,         /*          Usage Minimum (01h),            */
      0x29, 0x0C,         /*          Usage Maximum (0Ch),            */
      0x15, 0x00,         /*          Logical Minimum (0),            */
      0x25, 0x01,         /*          Logical Maximum (1),            */
      0x75, 0x01,         /*          Report Size (1),                */
      0x95, 0x0C,         /*          Report Count (12),              */
      0x81, 0x02,         /*          Input (Variable),               */
      0x75, 0x08,         /*          Report Size (8),                */
      0x95, 0x01,         /*          Report Count (1),               */
      0x81, 0x01,         /*          Input (Constant),               */
      0x05, 0x01,         /*          Usage Page (Desktop),           */
      0x09, 0x39,         /*          Usage (Hat Switch),             */
      0x25, 0x07,         /*          Logical Maximum (7),            */
      0x35, 0x00,         /*          Physical Minimum (0),           */
      0x46, 0x0E, 0x01,   /*          Physical Maximum (270),         */
      0x66, 0x40, 0x00,   /*          Unit (40h),                     */
      0x75, 0x04,         /*          Report Size (4),                */
      0x81, 0x42,         /*          Input (Variable, Null State),   */
      0x09, 0x30,         /*          Usage (X),                      */
      0x09, 0x31,         /*          Usage (Y),                      */
      0x15, 0x80,         /*          Logical Minimum (-128),         */
      0x25, 0x7F,         /*          Logical Maximum (127),          */
      0x46, 0xFF, 0x00,   /*          Physical Maximum (255),         */
      0x66, 0x00, 0x00,   /*          Unit,                           */
      0x75, 0x08,         /*          Report Size (8),                */
      0x95, 0x02,         /*          Report Count (2),               */
      0x81, 0x02,         /*          Input (Variable),               */
      0x09, 0x35,         /*          Usage (Rz),                     */
      0x95, 0x01,         /*          Report Count (1),               */
      0x81, 0x02,         /*          Input (Variable),               */
      0x09, 0x36,         /*          Usage (Slider),                 */
      0x16, 0x00, 0x00,   /*          Logical Minimum (0),            */
      0x26, 0xFF, 0x00,   /*          Logical Maximum (255),          */
      0x81, 0x02,         /*          Input (Variable),               */
      0x09, 0xBB,         /*          Usage (BBh),                    */
      0x15, 0x00,         /*          Logical Minimum (0),            */
      0x26, 0xFF, 0x00,   /*          Logical Maximum (255),          */
      0x35, 0x00,         /*          Physical Minimum (0),           */
      0x46, 0xFF, 0x00,   /*          Physical Maximum (255),         */
      0x75, 0x08,         /*          Report Size (8),                */
      0x95, 0x04,         /*          Report Count (4),               */
      0x91, 0x02,         /*          Output (Variable),              */
      0xC0,               /*      End Collection,                     */
      0xC0                /*  End Collection                          */

With extractor:

.. code:: bash

  $ python -m hrdc.descriptor.extractor -i hex broken2.hex

.. code:: python
  :number-lines:

  from hrdc.usage import *
  from hrdc.descriptor import *
  
  descriptor = TopLevel(
      Report(0,
          Collection(Collection.Application, desktop.Gamepad,
              Collection(Collection.Physical, desktop.Pointer,
                  Value(Value.Input, button.Button(1), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(2), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(3), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(4), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(5), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(6), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(7), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(8), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(9), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(10), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(11), 1, logicalMin = 0, logicalMax = 1),
                  Value(Value.Input, button.Button(12), 1, logicalMin = 0, logicalMax = 1),
                  Padding(Value.Input, 8),
                  Value(Value.Input, desktop.HatSwitch, 4, flags = Value.Variable|Value.NullState, logicalMin = 0, logicalMax = 7, physicalMin = 0, physicalMax = 270, unit = 64),
                  Value(Value.Input, desktop.X, 8, logicalMin = -128, logicalMax = 127, physicalMin = 0, physicalMax = 255),
                  Value(Value.Input, desktop.Y, 8, logicalMin = -128, logicalMax = 127, physicalMin = 0, physicalMax = 255),
                  Value(Value.Input, desktop.Rz, 8, logicalMin = -128, logicalMax = 127, physicalMin = 0, physicalMax = 255),
                  Value(Value.Input, desktop.Slider, 8, logicalMin = 0, logicalMax = 255),
                  Value(Value.Output, 0x100bb, 8, logicalMin = 0, logicalMax = 255),
                  Value(Value.Output, 0x100bb, 8, logicalMin = 0, logicalMax = 255),
                  Value(Value.Output, 0x100bb, 8, logicalMin = 0, logicalMax = 255),
                  Value(Value.Output, 0x100bb, 8, logicalMin = 0, logicalMax = 255),
              ),
          ),
      ),
  )
  
  if __name__ == "__main__":
      compile_main(descriptor)

Broken constructs:

- Hat switch unit is 0x40, which decodes to `No system, None^4
  (Length)`.  This is totally invalid (the person who did this
  probably mixed rows and columns in table from page 37 in
  `HID1_11`_);

- Hat switch goes from 0 to 7 (logical) and from 0° to 270°
  (physical), that means decoded values are 0°, 38.571°, 77.143°,
  115.714°, 154.286°, 192.857°, 231.429° and 270°.  On a compliant
  host, user may not be able to point North-West.  How could this go
  to the field uncatched ?

HID is hard to optimize
=======================

HID is hard to optimize by hand.  Once optimized, a report descriptor
is detious to edit by hand because author has to think about
interactions between local and global items.

HRDC contains an optimizer.  It can be used to rewrite existing
descriptors with identical meaning (including bugs above), but with
the canonical representation.

Let's try this on various report descriptors found in the wild.
I took various HID report descriptors from various devices, ran the
optimizer on them, compared report descriptor sizes.  There is always
some difference.

=========== ========== ============
Size before Size after Gain
=========== ========== ============
         32         30        \- 6 %
         61         60        \- 1 %
         73         61       \- 16 %
         97         45       \- 53 %
         98         73       \- 25 %
         98         73       \- 25 %
        101         85       \- 15 %
        103         87       \- 15 %
        106        102        \- 3 %
        108         91       \- 15 %
        108         91       \- 15 %
        116        113        \- 2 %
        117         82       \- 29 %
        119         92       \- 22 %
        119        100       \- 15 %
        142        112       \- 21 %
        146        116       \- 20 %
        148        118       \- 20 %
        148        118       \- 20 %
        148        118       \- 20 %
        148        142        \- 4 %
        149        135        \- 9 %
        152         98       \- 35 %
        156        104       \- 33 %
        166        164        \- 1 %
        174        125       \- 28 %
        178        155       \- 12 %
        184        159       \- 13 %
        196        168       \- 14 %
        214        204        \- 4 %
        214        211        \- 1 %
        217        199        \- 8 %
        246        234        \- 4 %
        259        232       \- 10 %
        266        237       \- 10 %
        275        234       \- 14 %
        326        293       \- 10 %
        326        293       \- 10 %
        409        350       \- 14 %
=========== ========== ============

Average gain: 15%

Conclusion
==========

There is no good reason we had to write HID report descriptors by hand
for so long!

.. _`HID1_11`: http://www.usb.org/developers/hidpage/HID1_11.pdf
.. _`HUT1_12v2`: http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
.. _`sibling tool`: https://github.com/DIGImend/hidrd/
