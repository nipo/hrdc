=====================
 HID Reader's Digest
=====================

Foreword
========

This text is a collection of thoughts about HID spec and
implementations in the wild, somewhere between observation of the
current situation after nearly 20 years of HID existence, and basic
rants about overlooked aspects of the Specification.

Introduction
============

HID got normalized in the USB-1.0 era.  This is a specification from
1990's, with a strong bias towards Microsoft Windows and Intel.  At
the time, machines had a few Megabytes of total RAM, there was nothing
to loose there.

Today, this may seem anecdotical, but this a various implications,
like using a single endianness (little) everywhere, at a time machines
where both little and big-endian, or preferring compactness over data
alignment.  Of course, everything is binary.

HID is a part of the enormous USB protocol stack.  It shares the same
design and phylosophy.  Everything has to be generic, flexible, future
proof.  At the time, PC suffered from too much custom hardware.  USB
was meant to be a generic one-size-fits-all transport.  HID was meant
to be the only generic protocol handling user interaction.

Genericity
==========

HID defines a framework for Human Interface Devices.  In the
specification, this includes Mice and Keyboards, but also VCR, Tape
Recorders, Graphical Equalizers, Graphical Displays.  Many of these
definitions were never actually used.

Designers of the specification were right about the genericity.  20
years later, Spec is still running and functionnal, and got adopted by
Bluetooth, Bluetooth Low Energy, Miracast (?), etc.  Genericity was
designed without compromise.

HID is a meta-framework that describes a method for describing input
(and output) messages format, from a device standpoint.  This was a
good idea, because this way, device implementor may pick and choose
what suits its needs among defined basic blocks, in order to get its
data interpreted by host.

Flexibility is on device side, genericity is on Host side.

Lack of examples
================

Problem with HID is its too big to be read, understood, and correctly
implemented the first time an implementor sees the spec.  There are
too many corner cases, too many disseminated rules, and too few
examples.

Today, we find ourselves in from of many devices where a driver is
still needed because the HID descriptor is useless (non-existant, full
of vendor-defined items, or simply broken), killing the whole point of
HID.  This situation could have been avoided if spec had code with
many examples to copy from.

Never forget device implementors are lazy like all other engineers,
but as device makers, they put result of their lazyness in ROMs,
rather than in updatable software...

Too much genericity
===================

In some aspects, genericity killed the whole purpose of the
specification.  Coupled with lack of examples, some parts are totally
overlooked by implementors.

The most relevant example is probably the Physical Interface Devices
page, meant for Force-Feedback applications.  Looking back nearly 20
years later, this part of the spec looks totaly over-engineered, to an
extent where nearly nobody actually implemented it correctly.  Most
devices with force-feedback actually require an Operating System
driver to circumvent the madness of this page.

Today, even Operating Systems HID stacks seem to have lost faith in
the PID page.

Rants
=====

Now, my personnal collection of rants.

"Multiple Instances of a Control"
---------------------------------

`HUT1_12v2`_, A.5, p. 132, defines the correct way to define a control
that exists more than once in a single device.

This has totally been overlooked by device implementors over the
years, to a point where today, guidelines from major OS actually
recommand something opposite to the spirit of the spec.  `Android
gamepad guidelines`_ suggests using `Z` and `rZ` for secondary thumb
stick.  Purpose of `Z` is for vertical axis (the one orthogonal to
both `X` and `Y`), and `rZ` is meant for *rotations* around the same
axis.  Nor for secondary `X/Y` couple.  This is broken.

.. _`HUT1_12v2`: http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
.. _`Android gamepad guidelines`: https://source.android.com/compatibility/android-cdd.pdf
