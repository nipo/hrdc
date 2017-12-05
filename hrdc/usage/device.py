from .usage import *

BatteryStrength = Usage("device.BatteryStrength", 0x60020, DV)
WirelessChannel = Usage("device.WirelessChannel", 0x60021, DV)
WirelessID = Usage("device.WirelessID", 0x60022, DV)
DiscoverWirelessControl = Usage("device.DiscoverWirelessControl", 0x60023, OSC)
SecurityCodeCharacterEntered = Usage("device.SecurityCodeCharacterEntered", 0x60024, OSC)
SecurityCodeCharacterErased = Usage("device.SecurityCodeCharacterErased", 0x60025, OSC)
SecurityCodeCleared = Usage("device.SecurityCodeCleared", 0x60026, OSC)
