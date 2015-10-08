from hrdc.usage import *
from hrdc.descriptor import *

bit_in = lambda x: Value(Value.Input, x, 1,
                         logicalMin = 0, logicalMax = 1)

bit_out = lambda x: Value(Value.Output, x, 1,
                          logicalMin = 0, logicalMax = 1)

key_range = lambda n: Value(Value.Input, usage = None, size = 8,
                            namedArray = UsageRange(keyboard.NoEvent, keyboard.KeypadHexadecimal),
                            logicalMin = 0, count = n)

keyboard = Collection(Collection.Application, desktop.Keyboard,
                      bit_in(keyboard.LeftControl),
                      bit_in(keyboard.LeftShift),
                      bit_in(keyboard.LeftAlt),
                      bit_in(keyboard.LeftGui),
                      bit_in(keyboard.RightControl),
                      bit_in(keyboard.RightShift),
                      bit_in(keyboard.RightAlt),
                      bit_in(keyboard.RightGui),

                      key_range(6),

                      bit_out(led.NumLock),
                      bit_out(led.CapsLock),
                      bit_out(led.ScrollLock),
                      )


if __name__ == "__main__":
    compile_main(keyboard)
    
