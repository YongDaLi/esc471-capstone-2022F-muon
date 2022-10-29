import os
import shutil

def writeEventToFile(counter, t, V):
    """
    This function stores the information of a measured event into a file
    with name output/event<i>.txt in the format
    t1,V11,V21,V31,V41
    t2,V12,V22,V32,V42
    ...
    Arguments:
        counter: The index of the file saving
        t: A list containing the values of times at which voltage is measured in s
        V: A list of size 4; each item is another list containing the voltages
           measured from the ith channel in V.
    """
    file = open("./waveform_fetch/events/event" + str(counter) + ".txt", "w")
    for i in range(len(t)):
        file.write(str(t[i]) + "," + str(V[0][i]) + "," + str(V[1][i]) + "," + str(V[2][i]) + "," + str(V[3][i]) + "\n")
    file.close()

def makeEventsDirectory():
    if os.path.exists("./waveform_fetch/events"):
        shutil.rmtree("./waveform_fetch/events")
    os.makedirs("./waveform_fetch/events")
