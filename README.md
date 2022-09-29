# Interface with Oscilloscope
Yong Da Li
date created: Thursday, September 29, 2022

This describes how to interface with the oscilloscope.

## Fancy new hardware
- https://www.tek.com/en/products/oscilloscopes/3-series-mdo
- it's got a touchscreen, so you've got to look at both the touchscreen and right-side physical buttons when looking for a function
- ex. the "utility" menu is on the top left of the touchscreen

- programming manual: https://www.tek.com/en/manual/oscilloscope/3-series-mixed-domain-oscilloscope-programmer-manual-3-series-mdo


## communication
The oscilloscope can do stuff like connect over ethernet or remote access. But for us, we're just sticking with USB. It's got a USB2.0 port on the back side, that you connect to your computer. Once you plug it in, it should be auto-detected by your computer. On Windows 11 device manager, it showed up as "MDO34" under other devices.

You'll need a VISA (Virtual Instrument Software Architecture) driver to talk to it. To download it it, follow the instructions on this page. Note that the bit-ness of the driver should match the same as your Python installation. 
- https://pyvisa.readthedocs.io/en/latest/faq/getting_nivisa.html#faq-getting-nivisa

The installation happens through NI (National Instruments). They install a bunch of other crap as well, but just go with the default settings out of fear that it'll screw up something later on. The install look a good 20min for Yong Da's laptop.

## Python interface
We're using a nice Python wrapper around the VISA library called PyVISA. Install it with:
```
pip install pyvisa
```

Your first program should be something like:
```
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
```


## more reading
The oscilloscope communication is based on IEEE488.2. You can read the manual for the full description of all commands.
- programming manual: https://www.tek.com/en/manual/oscilloscope/3-series-mixed-domain-oscilloscope-programmer-manual-3-series-mdo


## what the old code does
1. query current acquisition status, if error or stop handle it
2. get the waveform of the current status
