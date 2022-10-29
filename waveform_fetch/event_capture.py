import traceback
from Oscilloscope import Oscilloscope
from FileUtils import writeEventToFile, makeOutputDirectory
import numpy as np
from time import sleep

# Create a new events directory to save the captured events
makeEventsDirectory()

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

sleep(1) # Waiting to make sure all the above commands have run

print("Starting acquisition...")
oscilloscope.startAcquisition(True)

# Getting time
while oscilloscope.isAcquisitionRunning():
    continue
t = oscilloscope.getWaveForm(1)[0]
oscilloscope.startAcquisition(True)

counter = 0
maxCount = 20
while counter < maxCount:
    if not oscilloscope.isAcquisitionRunning():
        counter += 1
        try:
            V = [oscilloscope.getWaveForm(i+1)[1] for i in range(4)]
            writeEventToFile(counter, t, V)
            print("Captured event: " + str(counter) + "/" + str(maxCount))
        except:
            print("Error encountered on event " + str(counter) + ".")
            traceback.print_exc()
            print("**********************")
        oscilloscope.startAcquisition(True)

oscilloscope.stopAcquisition()
oscilloscope.close()
