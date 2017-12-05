from . import streamer
from ..stream.formatter import base as formatter
from ..stream import optimizer
import sys
import argparse

__all__ = ["compile_main"]

def compile_main(desc):

    import argparse

    parser = argparse.ArgumentParser(description='Compile a HID report descriptor')
    parser.add_argument("-o", "--output-format", metavar = "NAME", type = str,
                        default = "binary", help = "Output formatter name")

    parser.add_argument("output", type = argparse.FileType('w'),
                        default = "-",
                        nargs = "?", help = "Output file name")

    parser.add_argument("-N", "--no-optimize", action = "store_true",
                        help = "Dont optimize output stream")

    args = parser.parse_args()

    _formatter = formatter.Formatter.get(args.output_format)
    output = _formatter(args.output)

    if not args.no_optimize:
        output = optimizer.Optimizer.new(output)

    visitor = streamer.Streamer(output)
    desc.accept(visitor)
