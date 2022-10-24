'''
Haochen (Paul) Wang
Monday, October 24, 2022

Test script for count_events.py.
'''

import numpy as np
import random as rd
import count_events as count 

decayWindow = 5
S1ToS2Window = 5  # used for a time window for muon to travel between any two horizontal levels
S2ToElectronPeakWindow = decayWindow + S1ToS2Window

class muon:
    def __init__(self):
        self.timestamps = {1:[], 2:[], 3:[]}
        self.S1EntryTime = rd.randint(1,1000)
        self.timestamps[1].append(self.S1EntryTime)
        self.DecayedInS1 = (rd.randint(0,10)>9)
        self.EnteredS2 = (rd.randint(0,10)>1)
        self.S2EntryTime = -1
        self.DecayedInS2 = (rd.randint(0,10)>9)
        self.DecayedInAl = (rd.randint(0,10)>3)
        self.ElectronUp = (rd.randint(0,10)>3)
        self.ElectronS2EntryTime = -1
        self.ElectronS3EntryTime = -1

        if self.DecayedInS1:
            self.timestamps[1].append(self.S1EntryTime+rd.randint(1,decayWindow))

        else:
            if self.EnteredS2:
                self.S2EntryTime = self.S1EntryTime + rd.randint(1, S1ToS2Window)
                self.timestamps[2].append(self.S2EntryTime)
                if self.DecayedInS2:
                    self.timestamps[2].append(self.S2EntryTime + rd.randint(1,decayWindow))
                else:
                    # muon has reached Al plate
                    if self.DecayedInAl:
                        if self.ElectronUp:
                            self.ElectronS2EntryTime = self.S2EntryTime + rd.randint(1,decayWindow) + rd.randint(1,S1ToS2Window)
                            self.timestamps[2].append(self.ElectronS2EntryTime)
                        elif not self.ElectronUp:
                            self.ElectronS3EntryTime = self.S2EntryTime + rd.randint(1,decayWindow) + rd.randint(1,S1ToS2Window)
                            self.timestamps[3].append(self.ElectronS3EntryTime)
                         

    def getHistory(self):
        print("S1 Entry Time: ", self.S1EntryTime)
        print("Decayed in S1: ", self.DecayedInS1)
        print("Entered S2: ", self.EnteredS2)
        print("S2 Entry Time: ", self.S2EntryTime)
        print("Decayed in S2: ", self.DecayedInS2)
        print("Decayed in Al: ", self.DecayedInAl)
        print("Did the electron product go up? ", self.ElectronUp)
        print("Product electron S2 entry time: ", self.ElectronS2EntryTime)
        print("Product electron S3 entry time: ", self.ElectronS3EntryTime)

    def getTimestamps(self):
        return (np.array(self.timestamps[1]), np.array(self.timestamps[2]), np.array(self.timestamps[3]))

if __name__ == "__main__":
    u = muon()
    u.getHistory()
    data = u.getTimestamps()
    print(data)
    print("Up and down event counts: ", count.countEvents(data[0], data[1], data[2]))
