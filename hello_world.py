'''
Yong Da Li
Thursday, September 29, 2022

first PyVISA program that demonstrates you can talk to the oscilloscope
'''

import pyvisa

rm = pyvisa.ResourceManager()

# using the printed resources, open up the one that is the oscilloscope
print(rm.list_resources())

# change this as necessary
hardCodedResource = 'USB0::0x0699::0x052C::B014430::INSTR'
inst = rm.open_resource(hardCodedResource)

# send a query to see what the current acquisition settings are
query = "ACQuire?"
print(inst.query(query))

