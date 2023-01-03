from hrdc.usage import *
from hrdc.descriptor import *

descriptor = Collection(Collection.Application, sensors.Environmental,
    Collection(Collection.Physical, sensors.Environmental,
        Report(1,
            Value(Value.Input, sensors.EnvironmentalHumidity, 16, logicalMin = 0, logicalMax = 1400),
            Value(Value.Input, sensors.EnvironmentalTemperature, 8, logicalMin = 0, logicalMax = 100, count = 2),
            Value(Value.Input, sensors.EnvironmentalAtmosphericPressure, 8, logicalMin = 0, logicalMax = 100),
        ),
    ),
)
compile_main(descriptor)
