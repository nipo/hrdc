================================
 High-level descriptor language
================================

Let's take the following input file:

.. code:: python
  :number-lines:

  from hrdc.usage import *
  from hrdc.descriptor import *
  
  descriptor = Collection(Collection.Application, desktop.Mouse,
      Value(Value.Input, desktop.X, 8, flags = Value.Relative, logicalMin = -127, logicalMax = 127),
      Value(Value.Input, desktop.Y, 8, flags = Value.Relative, logicalMin = -127, logicalMax = 127),
      Value(Value.Input, button.Button(1), 1, logicalMin = 0, logicalMax = 1),
      Value(Value.Input, button.Button(2), 1, logicalMin = 0, logicalMax = 1),
      Value(Value.Input, button.Button(3), 1, logicalMin = 0, logicalMax = 1),
  )
  
  if __name__ == "__main__":
      compile_main(descriptor)

.. contents::

Glue
====

Imports
-------

.. code:: python

  from hrdc.usage import *
  from hrdc.descriptor import *

- `hrdc.usage` contains most HID Usage pages defined as
  `<page>.<Usage>` constants, see `usage constants`_.

- `hrdc.descriptor` contains all constructs for defining a high-level
  descriptor tree, see `hierarchical elements`_ and `data items`_.

Command-line handler
--------------------

.. code:: python

  if __name__ == "__main__":
      compile_main(descriptor)

At the end of the script, this code handles the command line only if
the script is invoked as main python script.  Using this construct has
a benefical side-effect: script may still be imported from another one
as a library.  This way, you may write various device descriptors and
merge them as a composite device through imports, but yet be able to
compile them separatly.

Data items
==========

Values
------

Values define Data items in a descriptor.  For each value declared,
all the relevant parameters should be defined, not considering if they
are actually serialized as local or global items.  There is no global
parameter in this descriptor format.

.. code:: python

  Value(way, usage, size,
        flags = Data | Variable | Absolute,
        logicalMin = 1, logicalMax = None,
        physicalMin = None, physicalMax = None,
        namedArray = None,
        unit = 0, unitExponent = 0,
        designator = 0,
        string = 0,
        count = 1,
        alignment = None)

way
  This is the Data Item type, either `Value.Input`, `Value.Output` or `Value.Feature`
usage
  This is the Usage for the value.  For named arrays, this is the
  usage for the surrounding logical collection.
size
  Data item size in bits
logicalMin, logicalMax
  Logical bounds, i.e. value range that device may encode in the
  `size`-bits data field
physicalMin, physicalMax
  Physical bounds, i.e. semantic value range reported to HID stack
  clients. If left to `None`, they will match logical bounds
namedArray
  Must be a `list` of Usage constants, or a `UsageRange` object.
  When set, value becomes a Named Array.  Physical bounds are invalid
  for a Named Array, and only `logicalMin` is relevant to set the
  logical value for first array item.  This defaults to 1 but may be
  set to another value for specific purposes (0 most of the time)
unit
  Physical value unit, see units_ below
unitExponent
  Base-10 exponent to apply to physical value
designator
  Designator index, for physical descriptors
string
  String index, for string descriptors
count
  Useful for array-of-Named-Arrays only, like in keyboard descriptors
alignment
  Alignment to enforce before inserting this value

Padding
-------

`Padding()` is a short-hand for constant `Value()` for a given bit
width.

For instance the following values will be on two consecutive bytes,
each at lower bit:

.. code:: python

  Value(Value.Input, button.Button(1), 1, logicalMin = 0, logicalMax = 1),
  Padding(Value.Input, 7),
  Value(Value.Input, button.Button(2), 1, logicalMin = 0, logicalMax = 1),

Alignment
---------

`Align()` construct is a short-hand for `Padding()` where report data
is aligned on next bit size boundary.

For instance the following values will be on two consecutive bytes,
each at lower bit:

.. code:: python

  Value(Value.Input, button.Button(1), 1, logicalMin = 0, logicalMax = 1),
  Align(Value.Input, 8),
  Value(Value.Input, button.Button(2), 1, logicalMin = 0, logicalMax = 1),

Hierarchical elements
=====================

Collection
----------

`Collection()` generates `Collection` and `End Collection` global
items.  This hierarchical object needs a type (`Physical`,
`Application`, `Logical`, `Report`, `NamedArray`, `UsageSwitch` or
`UsageModifier`) and a Usage constant.

.. code:: python

  Collection(Logical, desktop.Keyboard,
    Value(...),
    ...
  )

TopLevel
--------

`TopLevel()` is a pseudo-collection that generates no Item, but allows
to have more than one top-level collection.

.. code:: python

  TopLevel(
    Collection(Logical, desktop.Keyboard,
      Value(...),
      ...
    ),
    Collection(Logical, consumer.ConsumerControl,
      Value(...),
      ...
    ),
  )

Report
------

`Report()` is a collection that generates no Item, but sets report ID
for subtree.

.. code:: python

  Collection(Logical, desktop.Keyboard,
    Report(1,
      Value(...),
      Value(...),
      Value(...),
    ),

    Report(2,
      Value(...),
      Value(...),
      Value(...),
    ),
  )

Usage constants
===============

Usage constants are defined as symbolic values.  They refer to objects
that behave like ints, but also have a stringifiable correspondance:

.. code:: python

  >>> from hrdc.usage import *
  >>> desktop.X
  <hrdc.usage.usage.Usage instance at 0x104f523f8>
  >>> str(desktop.X)
  'desktop.X'
  >>> hex(int(desktop.X))
  '0x10030'

`Usage` class can also resolve named constants from the numerical
value:

.. code:: python

  >>> from hrdc.usage import *
  >>> u = Usage.lookup(0x10031)
  >>> str(u)
  'desktop.Y'

For Named-Array Values, constants can be assembled in a Python list,
but when numerous contiguous Usage constants have to be used, you may
use `UsageRange` utility.  It behaves like a Python list (operators
`len`, `[]` and iterable), but avoids explicitly enumerating all
intermediate constants.  For instance, a PC keyboard key value is
defined as:

.. code:: python

  Value(Value.Input, usage = None, size = 8,
        namedArray = UsageRange(keyboard.NoEvent, keyboard.KeypadHexadecimal),
        logicalMin = 0)

.. code:: python

  >>> from hrdc.usage import *
  >>> r = UsageRange(keyboard.NoEvent, keyboard.KeypadHexadecimal)
  >>> str(r[0])
  'keyboard.NoEvent'
  >>> str(r[32])
  'keyboard.ThreeAndNumber'

Units
=====

Units can either be constructed from `system` and various dimensions
(as in spec), or from well-known constants:

.. code:: python

  >>> from hrdc.descriptor import *
  >>> si_length = Unit.SILinear | Unit.length(1)
  >>> hex(si_length)
  '0x11'
  >>> si_length == Unit.Centimeter
  True

Dimensions are: length, mass, time, temperature, current,
luminousintensity.  They take an exponent in range [-8, 7] as
argument.

Well known constants are: Centimeter, Radian, Inch, Degree, Gram,
Slug, Second, Kelvin, Fahrenheit, Ampere, Candela, CmPerSec, Momentum,
G, Newton, Joule, Voltage.
