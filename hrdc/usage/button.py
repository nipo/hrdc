from usage import *

def Button(n):
    return Usage("button.Button(%d)" % int(n), 0x90000 + int(n),
                 Sel, OOC, MC, OSC)

for i in range(128):
    Button(i)
