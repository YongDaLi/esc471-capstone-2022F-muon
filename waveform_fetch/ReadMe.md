# The Waveform Acquisition Script Guide

We use the `event_capture.py` to store information from the Oscilloscope.

Then the `event-analyzer.py` script can be used to convert the stored information into information understandable to Paul's code for determining the direction in which the positron was emanated.

## Event Capture

To run this first connect the oscilloscope to the Tektronix Series 3 Oscilloscopes. Preferably connect the scintillators from top to bottom to channels 1 to 4 respectively. It is in particular important to connect the upper most scintillator to Channel 1; the trigger is set on that channel (Recall that we only assume a muon has reached the telescope if the top scintillator is triggered, and so we only trigger when the top scintillator detects something).

At this step make sure all channels 1-4 are displayed on the oscilloscope. To do this press the 1-4 buttons on the vertical command group until their waveforms are visible on the screen.

After this simply run the `event_capture.py` script. This will record the relevant information from the oscilloscope to the `events` directory. The number of stored events is equal to `maxCount`.

### Trouble Shooting

If the code freezes when trying to connect to the oscilloscope, turn the oscilloscope off and on; do not try to close the program from the computer.

## Event Analyzers

This script can only be run after the event capturer script is run; the outputs of that script are the inputs of this script.

The purpose of this script is to detect the peaks in the stored waveforms and to list the detected peaks, their relative time, and their respective channel in a text file in `output.txt`. This is what Paul's code should use to determine the positron directions.

## Output

The file `output.txt` contains just as many lines as events stored.

Each line is a series of numbers as follows:

```
c1, t1, c2, t2, c3, t3, ...
```

Which means at channel `ci` a peak was detected at `ti`. These numbers are sorted by time, so it is guaranteed that `ti < t(i+1)`.
