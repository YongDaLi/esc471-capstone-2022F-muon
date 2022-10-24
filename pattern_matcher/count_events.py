'''
Haochen (Paul) Wang
Saturday, October 22, 2022

Given the data acquired from the three oscilloscope channels, corresponding to the three scintillators (2 up ones labelled S1 and S2, 1 down one labelled S3), count the number of up and down events. S2 and S3 are pancakes.

An up event is a muon decay event whose daughter electron is emitted upwards.
A down event is a muon decay event whose daughter electron is emitted downwards. 

The oscilloscope data records the timestamps when peaks occur.
For example, s1=[0.1829, 32.4746, 33.3245, 74.7817] means scintillator 1 detected four peaks, at these four points in time.

Note that a muon would trigger a peak (a) upon entering a scintillator, and (b) upon decaying in a scintillator.
'''

'''
Chef's kiss:
"python3 count_events.py" runs the script without debug prints. 
"python3 count_events.py -debug" runs the script with debug prints.'''

# TODO: the logic here is very dirty and error-prone. Think about a better counting logic.
 
import sys
import numpy as np

decayWindow = 5    # muon life time is 2.2 us; set a somewhat higher threshold for filtering out decays in the same scintillator
S1ToS2Window = 5   # time needed for a muon to travel from scintillator 1 to scintillator 2
S2ToElectronPeakWindow = decayWindow + S1ToS2Window


def log(x):
    # "python3 count_events.py" would run the script without debug prints. 
   # "python3 count_events.py -debug" would run the script with debug prints.  
    if "-debug" in sys.argv:
        print(x)


def wouldDecay(sc, t, window):
    #Given a scintillator data sc and a peak at time point t, check that this peak is a muon entering a scintillator where it then immediately decayed
    if t==len(sc)-1:
        return False
    return ((sc[t+1] - sc[t]) <= window)



def isDecay(sc, t, window):
    #Given a scintillator data sc and a peak at time point t, check that this peak is a muon decaying in this scintillator
    if t==0:
        return False
    return ((sc[t] - sc[t-1]) <= window)



def enteredS2(S1, S2, t, S2EntryPeak):
    # Check if the muon entering S1 at t later entered S2
    # Record the index in S2 when the muon entered S2
    for i in range(len(S2)):
        if S2[i] < S1[t]:
            continue
        if (S2[i]-S1[t]) < S1ToS2Window:
            # note that integers are not mutable in python, so need to return via argument by a list
            S2EntryPeak.clear()
            S2EntryPeak.append(i)
            return True
    return False


def decayedDown(S2, S3, t):
    # Check if the muon entering S2 at t later decayed and emitted the electron down into S3
    for i in range(len(S3)):
        if S3[i] < S2[t]:
            continue
        if (S3[i]-S2[t]) < S2ToElectronPeakWindow and (S3[i]-S2[t]) > decayWindow/3:  # note that decayWindow is a upper threshold, but there we want a lower threshold. Use /3 as extimate.
            return True
    return False


def decayedUp(S2, t):
    # Check if the muon entering S2 at t later decayed and emitted the electron up back into S2
    for i in range(t+1, len(S2)):
        if (S2[i]-S2[t]) < S2ToElectronPeakWindow and (S2[i]-S2[t]) > decayWindow/3:
            return True
    return False
    
def countEvents(S1,S2,S3):
    up = 0
    down = 0
    for i in range(0, len(S1), 1):
        # exclude muons that decayed in S1
        if wouldDecay(S1, i, decayWindow) or isDecay(S1, i, decayWindow):
            # TODO: better logging for more than one log item
            log(S1[i])
            log(" is omitted\n")
            continue

        # exclude muons that didn't enter S2
        S2EntryPeak = []
        #log(enteredS2(S1, S2, i, S2EntryPeak))
        if not enteredS2(S1, S2, i, S2EntryPeak):
            log(S1[i])
            log(" is omitted\n")
            continue

        # exclude muons that decayed in S2
        log(S2EntryPeak)
        log(wouldDecay(S2, S2EntryPeak[0], decayWindow/3))
        if wouldDecay(S2, S2EntryPeak[0], decayWindow/3):
            log(S1[i])
            log(" is omitted\n")
            continue

        # At this point we have muons that passed through S1 and S2 and ready to decay in the aluminium plate.
        log("reached Al plate") 
        if decayedDown(S2, S3, S2EntryPeak[0]):
            log(S1[i])
            log(" is ready to decay down")
            down += 1
        elif decayedUp(S2, S2EntryPeak[0]):  # elif so don't double count a decay in metal plate for both down and up
            log(S1[i])
            log(" is ready to decay up")
            up += 1
    return up,down



if __name__ == "__main__":
    # very premature test, expect 2 up and 1 down
    #S1 = np.array([0.3, 1.5, 10.7, 30, 70, 100, 103, 144])
    #S2 = np.array([13.2, 33, 39, 73, 77, 147, 156])
    #S3 = np.array([19.8, 51, 53, 78])
    S1 = np.array([939])
    S2 = np.array([942])
    S3 = np.array([948])
    print(countEvents(S1, S2, S3)) 
