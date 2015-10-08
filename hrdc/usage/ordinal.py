from usage import *

def Ordinal(n):
    return Usage("ordinal.Ordinal(%d)" % int(n), 0xa0000 + int(n), CL)

for i in range(128):
    Ordinal(i)
