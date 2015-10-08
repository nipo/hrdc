from hrdc.usage import *
from hrdc.descriptor import *

battery = Collection(Collection.Application, consumer.ConsumerControl,
                     Collection(Collection.Logical, desktop.Keyboard,
                                Value(Value.Input, device.BatteryStrength, 8,
                                      logicalMin = 0, logicalMax = 100)
                                )
                     )


if __name__ == "__main__":
    compile_main(battery)
    
