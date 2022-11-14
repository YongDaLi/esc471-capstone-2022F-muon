import pyvisa
from enum import Enum
import numpy as np

class Oscilloscope:
    """
    Tektronix Series 3 Oscilloscope
    Programming Manual: https://download.tek.com/manual/3-MDO-Oscilloscope-Programmer-Manual-077149800.pdf
    """

    class TriggerType(Enum):
        Edge = "EDG"
        Logic = "LOG"
        PulseWidth = "PULS"
        Bus = "BUS"
        Video = "VID"

    class TriggerMode(Enum):
        Normal = "NORM"
        Automatic = "AUTO"

    class AcquisitionMode(Enum):
        Peak = "PEAK"
        Sample = "SAM"

    def __init__(self, oscilloscopeHardCoded):
        self.inst = None

        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(oscilloscopeHardCoded)
        if (self.inst == None):
            print("Can't connect to the oscilloscope")
            exit()

        self.defaultSetup()
        self.setupAcquisitionParameters()

    def defaultSetup(self):
        self.inst.write("DEFaultsetup")

    def setupAcquisitionParameters(self):
        """
        This setups up the required prerequisites for reading waveforms from the scope.
        """
        self.inst.write("DATa:STARt 1")
        self.inst.write("DATa:STOP 10000")
        self.inst.write("DATa:ENCd ASCIi")
        self.inst.write("DATa:WIDth 1")
        self.inst.write("HEADer 1")
        self.inst.write("VERBose 1")

        # This will make sure all the commands above have run
        while True:
            if self.inst.query("VERBOSE?")[-2] == "1": # the last char is not the number
                break

        wfmOut = self.inst.query("WFMOutpre?")
        wfmOut = wfmOut.strip(":").strip("\n").split(";")
        for param in wfmOut:
        	if "YMULT" in param:
        		self.ymult = float(param.split(" ")[1])
        	elif "XINCR" in param:
        		self.xincr = float(param.split(" ")[1])
        	elif "NR_PT" in param:
        		self.nr_pt = float(param.split(" ")[1])
        	elif "XZERO" in param:
        		self.xzero = float(param.split(" ")[1])
        	elif "YZERO" in param:
        		self.yzero = float(param.split(" ")[1])

    def startAcquisition(self):
        self.inst.write("ACQ:STATE ON")

    def startAcquisition(self, stopAfter):
        if stopAfter:
            self.inst.write("Acquire:StopAfter SEQUENCE")
        self.inst.write("ACQ:STATE ON")

    def stopAcquisition(self):
        self.startAcquisition(False)

    # Numbers must be provided in NR3 notation: 250E-3
    def setTrigger(self, type: TriggerType, channelNumber, voltage: str, mode: TriggerMode, holdoff: str, acquisitionMode: AcquisitionMode):
        self.inst.write("TRIG:A:TYPE " + type.value)
        self.inst.write("TRIGger:A:EDGE:SOUrce CH" + str(channelNumber))
        self.inst.write("TRIG:A:LEV:CH" + str(channelNumber) + " " + voltage)
        self.inst.write("TRIG:A:MOD " + mode.value)
        self.inst.write("TRIG:A:HOLD:TIM " + holdoff)

        self.inst.write("ACQ:MOD " + acquisitionMode.value)

    def getWaveForm(self, channelNumber):
        self.inst.write("DATa:SOUrce CH" + str(channelNumber))

        curve = [float(s) for s in self.inst.query("CURV?").strip(":CURVE").strip("\n").split(",")]

        t = np.linspace(0,(self.xincr*self.nr_pt), int(self.nr_pt)) + self.xzero
        V = np.array(curve) * self.ymult + self.yzero

        return [t, V]

    def setHorizontalScale(self, timePerDivision: str):
        self.inst.write("HOR:SCA " + timePerDivision)

    def isAcquisitionRunning(self):
        res = self.inst.query("ACQUIRE:STATE?")

        return res[-2] == "1"

    def close(self):
        self.inst.close()
