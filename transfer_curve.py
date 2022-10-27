"""
Yong Da Li
Thursday, September 29, 2022

transfers a curve and plots it
"""
import numpy as np
import matplotlib.pyplot as plt
import pyvisa

# connect to scope
rm = pyvisa.ResourceManager()
print(rm.list_resources())
hardCodedResource = "USB0::0x0699::0x052C::B014430::INSTR"
inst = rm.open_resource(hardCodedResource)

# setup data output
inst.write("DATa:SOUrce CH1")
inst.write("DATa:STARt 1")
inst.write("DATa:STOP 10000")
inst.write("DATa:ENCd ASCIi")
inst.write("DATa:WIDth 1")
inst.write("HEADer 1")
inst.write("VERBose 1")

# check output format
wfmOut = inst.query("WFMOutpre?")

# need to parse it
# wfmOut = ':WFMOUTPRE:BYT_NR 1;BIT_NR 8;ENCDG ASCII;BN_FMT RI;BYT_OR MSB;WFID "Ch1, DC coupling, 1.000V/div, 400.0us/div, 10000 points, Sample mode";NR_PT 10000;PT_FMT Y;PT_ORDER LINEAR;XUNIT "s";XINCR 400.0000E-9;XZERO -2.0000E-3;PT_OFF 0;YUNIT "V";YMULT 40.0000E-3;YOFF 0.0E+0;YZERO 0.0E+0;DOMAIN TIME;WFMTYPE ANALOG;CENTERFREQUENCY 0.0E+0;SPAN 0.0E+0;REFLEVEL 0.0E+0\n'

wfmOut = wfmOut.strip(":").strip("\n").split(";")

# parse parameters
for param in wfmOut:
    if "YMULT" in param:
        print(param)
        ymult = float(param.split(" ")[1])

    if "XINCR" in param:
        print(param)
        xincr = float(param.split(" ")[1])

    if "NR_PT" in param:
        print(param)
        nr_pt = float(param.split(" ")[1])

    if "XZERO" in param:
        print(param)
        xzero = float(param.split(" ")[1])

    if "YZERO" in param:
        print(param)
        yzero = float(param.split(" ")[1])


# get data
curve = inst.query("CURVE?")

# clean up data
curve = curve.strip(":CURVE ").strip("\n").split(",")
for i in range(len(curve)):
    curve[i] = float(curve[i])


# load previous session
# import pickle
# with open("20220929.pkl", "rb") as f:
# 	bk = pickle.load(f)

# curve = bk['curve']
# wfmOut = bk['wfmOut']

# construct real curves
curve = np.array(curve) * ymult + yzero
x = np.linspace(0, (xincr * nr_pt), int(nr_pt)) + xzero

plt.plot(x, curve)
plt.xlabel("time [s]")
plt.ylabel("voltage [V]")
plt.show()
