import traceback
from Oscilloscope import Oscilloscope
from FileUtils import writeEventToFile, makeOutputDirectory
import numpy as np
from time import sleep

makeOutputDirectory()

# This should be potentially altered. The hardcoded address can be found
# by checking NI Max.
oscilloscopeHardCoded = 'USB0::0x0699::0x052C::B014443::INSTR'

print("Connecting to the oscilloscope...")
oscilloscope = Oscilloscope(oscilloscopeHardCoded)

print("Initializing the Oscilloscope...")
oscilloscope.stopAcquisition()
oscilloscope.setTrigger(
    Oscilloscope.TriggerType.Edge,
    1,
    "-250E-3",
    Oscilloscope.TriggerMode.Normal,
    "20E-9",
    Oscilloscope.AcquisitionMode.Peak
)
oscilloscope.setHorizontalScale("4E-6")

sleep(1000) # Waiting to make sure all the above commands have run

print("Starting acquisition...")
oscilloscope.startAcquisition()

# Getting time
t = oscilloscope.getWaveForm(1)[0]

counter = 0
maxCount = 100
while counter < maxCount:
    if oscilloscope.isAcquisitionRunning() == False:
        counter += 1
        try:
            V = [oscilloscope.getWaveForm(i)[1] for i in range(4)]
            writeEventToFile(counter, t, V)
            print("Captured event: " + str(counter) + "/" + str(maxCount))
            oscilloscope.startAcquisition()
        except:
            print("Error encountered on event " + str(counter) + ".")
            traceback.print_exc()
            print("**********************")

oscilloscope.stopAcquisition()
