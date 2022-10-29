import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from scipy.signal import savgol_filter, find_peaks

eventsDirectory = "./waveform_fetch/events"
peaksDirectory = "./waveform_fetch/peaks"
peakMin = -3
peakMax = -0.05
peakThreshold = 1e-6

def readFile(address):
    file = open(eventsDirectory + "/" + address, "r")
    lines = file.readlines()

    t = []
    V = [[] for i in range(4)]
    for line in lines:
        s = line.split(',')
        t += [float(s[0])]
        for j in range(4):
            V[j] += [float(s[j+1])]

    return [t, V]

def findPeaks(t, V):
    """
    Returns the indices of the peaks
    """
    dt = t[1] - t[0]
    peakSci = find_peaks(V, height=[peakMin, peakMax])[0]
    peaks = []
    ll = []
    for p in peakSci:
        if len(ll) == 0:
            ll += [p]
        elif (p - ll[0]) * dt < peakThreshold:
            ll += [p]
        else:
            peaks += [int(sum(ll) / len(ll))]
            ll = []

    if len(ll) != 0:
        peaks += [int(sum(ll) / len(ll))]

    return peaks

if not os.path.exists(eventsDirectory):
    print("No event directory found")
    exit()

if os.path.exists(peaksDirectory):
    shutil.rmtree(peaksDirectory)

os.makedirs(peaksDirectory)

eventFiles = [s for s in os.listdir(eventsDirectory) if s.startswith("event") and s.endswith(".txt")]
eventFiles = sorted(eventFiles, key=lambda s : int(s.split("t")[1].split(".")[0]))

info = []
for (i, address) in enumerate(eventFiles):
    print("Event " + str(i+1) + "/" + str(len(eventFiles)))

    [t, V] = readFile(address)
    info += [[]]

    fig, ax = plt.subplots(2, 2, figsize=(12,7))

    for j in range(4):
        n = j // 2
        m = j % 2

        peaks = findPeaks(t, V[j])

        ax[n, m].set_title("Channel " + str(j+1) + "; " + str(len(peaks)) + " Peaks")
        ax[n, m].plot(t, V[j], c=(0,0,0), linewidth=0.5)
        for p in peaks:
            ax[n, m].axvline(t[p], c=(1,0,0), linewidth=1.5)
            info[-1] += [(j+1, t[p])]

    plt.savefig(peaksDirectory + "/" + address.split('.')[0] + ".jpg")

sinfo = [sorted(d, key=lambda r : r[1]) for d in info]
lines = [",".join([str(l[0]) + "," + str(l[1]) for l in d]) for d in sinfo]

outputFile = open("./waveform_fetch/output.txt", "w")
for line in lines:
    outputFile.write(line + "\n")
