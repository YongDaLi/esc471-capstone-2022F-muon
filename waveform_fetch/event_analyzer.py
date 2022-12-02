import traceback
from Oscilloscope import Oscilloscope
from FileUtils import writeEventToFile, makeEventsDirectory, readFile
from time import sleep
import matplotlib.pyplot as plt
import os
import shutil

eventsDirectory = "./events"
peaksDirectory = "./peaks"
peakMax = [0.06, -0.15]  # Threshold that the voltate should cross from below to be considered a peak; different for each channel
peakThreshold = [0.5e-6, 1e-6]   # The minimum distance considered between peaks; different for each channel as each scintillator 
                                 # could have a different response time.
                                 
saveAllData = False        # If False, we only save events in which the muon decays.

def newOscilloscope():
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
        "-120E-3",
        Oscilloscope.TriggerMode.Normal,
        "20E-9",
        Oscilloscope.AcquisitionMode.Peak
    )
    oscilloscope.setHorizontalScale("2E-6")
    
    sleep(1) # Waiting to make sure all the above commands have run
    
    return oscilloscope


def findPeaks(channel, t, V):  # Returns the avg index, not time
    """
    Returns the indices of the peaks
    """
    dt = t[1] - t[0]
    
    peaks = []
    flag = False
    lastPeak = None
    for (i, v) in enumerate(V):
       if v <= peakMax[channel] and (len(peaks) == 0 or (i - peaks[-1]) * dt > peakThreshold[channel]):
          flag = True
       if flag:
          if lastPeak is None or lastPeak[1] > v:
              lastPeak = (i, v)
        
          if v > peakMax[channel]:
              peaks += [lastPeak[0]]
              lastPeak = None
              flag = False
         

    return peaks


tt = None
def recordEvent(counter, maxCount):
    global tt
    # Getting time
    if tt is None:
        oscilloscope.startAcquisition(True)
        while oscilloscope.isAcquisitionRunning():
            continue
        tt = oscilloscope.getWaveForm(1)[0]
        
    oscilloscope.startAcquisition(True)
    while oscilloscope.isAcquisitionRunning():
        continue
    
    try:
        V = [oscilloscope.getWaveForm(i+1)[1] for i in range(2)]
        return [tt, V]
    except:
        print("Error encountered on event " + str(counter) + ".")
        traceback.print_exc()
        print("**********************")
        return None
    
def setupDirectories():
    # Create a new events directory to save the captured events
    makeEventsDirectory()
    
    if os.path.exists(peaksDirectory):
        shutil.rmtree(peaksDirectory)
    
    os.makedirs(peaksDirectory)
    
def checkIfRelevant(info): # [(channel num, peak time)]
    if len(info) < 2: # If only 1 peak, the muon must have crossed only the top scintillator.
        return False
    
    # Feel free to add more terms here, depending on what you want to measure; for example you can filter out events in which the
    # second scintillator has two peaks.
    
    return True

setupDirectories()
oscilloscope = newOscilloscope()

print("Starting acquisition...")
maxCount = 520000   # Number of measurements to take; many of these could be discarded if saveAllData is False
# Note that we have roughly 50 counts per minute, so for running this for days we need maxCount to be on the order of ~100,000s.

info = [] # A list of lists, each list member has a number of pairs comprised of the 1) channel index and 2) peak time.
if saveAllData:
    print("Saving all measurements...")
else:
    print("Saving only measurements that pass through the filter (are relevant)...")
for counter in range(1, maxCount+1):    
    result = recordEvent(counter, maxCount)
    if result is None: # If unsuccessful
        print("Skipping the analysis of event " + str(counter) + "...")
        continue
    t = result[0]
    V = result[1]
    
    print("Event Analyzed " + str(counter) + "/" + str(maxCount))

    fig, ax = plt.subplots(2, 1, figsize=(12, 7))
    newInfo = []
    for j in range(2):
        peaks = findPeaks(j, t, V[j])

        ax[j].set_title("Channel " + str(j + 1) + "; " + str(len(peaks)) + " Peaks")
        for p in peaks:
            ax[j].axvline(t[p], c=(1, 0, 0), linewidth=1.5)
            newInfo += [(j + 1, t[p])] # (channel number, peak time)
        ax[j].plot(t, V[j], c=(0, 0, 0), linewidth=0.5)

    if saveAllData or checkIfRelevant(newInfo):
        info += [newInfo]
        
        address = eventsDirectory + "/event" + str(len(info)) + ".txt"
        writeEventToFile(address, tt, V)
    
        address = peaksDirectory + "/event" + str(len(info)) + ".jpg"
        plt.savefig(address)
        print("Event " + str(counter) + " saved.")
    else:
        print("Measurement " + str(counter) + " was irrelevant; not saving the result.")
    
    plt.close(fig)

sinfo = [sorted(d, key=lambda r: r[1]) for d in info]
lines = [",".join([str(l[0]) + "," + str(l[1]) for l in d]) for d in sinfo]

outputFile = open("./output.txt", "w")
for line in lines:
    outputFile.write(line + "\n")
    
oscilloscope.stopAcquisition()
oscilloscope.close()