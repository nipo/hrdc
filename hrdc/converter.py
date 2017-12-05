from .stream import *
import sys
import argparse

def _main():
    cmdline = argparse.ArgumentParser(description='Convert a HID report descriptor')

    cmdline.add_argument("-i", "--input-format", metavar = "NAME", type = str,
                        default = "binary", help = "Input parser name")

    cmdline.add_argument("-o", "--output-format", metavar = "NAME", type = str,
                        default = "binary", help = "Output formatter name")

    cmdline.add_argument("input", type = argparse.FileType('r'),
                         default = "-",
                         nargs = "?", help = "Input file name")

    cmdline.add_argument("output", type = argparse.FileType('w'),
                         default = "-",
                         nargs = "?", help = "Output file name")

    cmdline.add_argument("-O", "--optimize", action = "store_true",
                        help = "Optimize stream")

    args = cmdline.parse_args()

    _parser = parser.Parser.get(args.input_format)
    _formatter = formatter.Formatter.get(args.output_format)

    stream = _formatter(args.output)

    if args.optimize:
        stream = optimizer.Optimizer.new(stream)

    p = _parser(args.input, stream)
    p.read()

if __name__ == '__main__':
    _main()
