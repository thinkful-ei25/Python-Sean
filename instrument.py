import ctcsound; 

# csound instance
cs = ctcsound.Csound() 

options = '''
<CsOptions>
  -odac
</CsOptions>
'''

header = '''
sr = 44100 ; sample rate
kr = 4410 ; control rate (allows slower moving singal less compute time)
ksmps = 10  ; control period (sr / kr)
nchnls = 2; number of channels
'''


csd = '''
<CsoundSynthesizer>

<CsOptions>
  -odac
</CsOptions>

<CsInstruments>
sr = 44100 ; sample rate
kr = 4410 ; control rate (allows slower moving singal less compute time)
ksmps = 10  ; control period (sr / kr)
nchnls = 1 ; number of channels


          instr 1; 
a1        oscil   25, 440, 1
          out     a1
          endin


</CsInstruments>

<CsScore>
f1   0    2048 10   1                                                                ; Sine
f2   0    2048 10   1    0.5  0.3  0.25 0.2  0.167     0.14      0.125     .111      ; Sawtooth
f3   0    2048 10   1    0    0.3  0    0.2  0         0.14      0         .111      ; Square
f4   0    2048 10   1    1    1    1    0.7  0.5       0.3       0.1                 ; Pulse



e                     ; indicates the end of the score
</CsScore>
</CsoundSynthesizer>
'''

ret = cs.compileCsdText(csd)
if ret == ctcsound.CSOUND_SUCCESS:
  cs.start()
  cs.perform()
  cs.reset()