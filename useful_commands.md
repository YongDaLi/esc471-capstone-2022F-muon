miscellaneous group
===================
BUSY? Returns oscilloscope status
*CLS Clears status
ALLEv? Returns all events and their messages


waveform transfer command group
===============================
:DATa:SOUrce CH1 Sets the source waveform to be transferred to Channel 1.
:DATa:STARt 1 This, along with DATa:STOP, specifies the portion of the waveform record that will
be transferred .
:DATa:STOP 10000
:DATa:ENCdg ASCIi Sets the data format to ASCII. (This command replaces WFMOutpre:ENCdg,
WFMOutpre:BN_Fmt and WFMOutpre:BYT_Or with a single command.)
:DATa:WIDth 1 Sets 1 byte per point (same as WFMOutpre:BYT_Nr).
:HEADer 1 Turning on HEADer and VERBose will allow you to view the WFMOutpre?
parameters in context.
:VERBose 1
:WFMOutpre? The WFMOutpre? query provides the information needed to interpret the waveform
data point information that will be returned from the CURVe query.
:HEADer 0 You may want to turn the header off before doing the CURVe query, because with
the header on, a CURVe query will return the CURVe command header followed by
a space and the ASCII waveform data.
:CURVe? Transfers the data points



notes
=====
>>> inst.query("WFMO?")
':WFMOUTPRE:BYT_NR 1;BIT_NR 8;ENCDG ASCII;BN_FMT RI;BYT_OR MSB;WFID "Ch1, DC coupling, 1.000V/div, 400.0us/div, 10000 points, Sample mode";NR_PT 100;PT_FMT Y;PT_ORDER LINEAR;XUNIT "s";XINCR 400.0000E-9;XZERO -2.0000E-3;PT_OFF 0;YUNIT "V";YMULT 40.0000E-3;YOFF 0.0E+0;YZERO 0.0E+0;DOMAIN TIME;WFMTYPE ANALOG;CENTERFREQUENCY'

:WFMOUTPRE:BYT_NR 1
BIT_NR 8
ENCDG ASCII
BN_FMT RI
BYT_OR MSB
WFID "Ch1, DC coupling, 1.000V/div, 400.0us/div, 10000 points, Sample mode"
NR_PT 100
PT_FMT Y
PT_ORDER LINEAR
XUNIT "s"
XINCR 400.0000E-9
XZERO -2.0000E-3
PT_OFF 0
YUNIT "V"
YMULT 40.0000E-3	# Specifies the vertical scale multiplying factor used to convert the incoming
data points from digitizing levels into the units specified above.
YOFF 0.0E+0
YZERO 0.0E+0
DOMAIN TIME
WFMTYPE ANALOG
CENTERFREQUENCY