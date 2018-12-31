import ctcsound

# csound instance
cs = ctcsound.Csound() 
# print('cs', cs); 

#csound & ctcsound version
v, va = cs.version(), cs.APIVersion()
print("Raw version values: {}, {}".format(v, va))

# setup only
# i-rate variables, changed at the note rate
# k-rate variables, changed at the control signal rate
# a-rate variables, changed at the audio signal rate

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

          instr 2
a1        oscil     p4, p5, 1      ; p4=amp
          out       a1             ; p5=freq
          endin

         instr 3                       ; p3=duration of note
k1       linen     p4, p6, p3, p7      ; p4=amp
a1       oscil     k1, p5, 1           ; p5=freq
         out       a1                  ; p6=attack time
         endin                         ; p7=release time


</CsInstruments>

<CsScore>
f1  0   4096    10 1  ; use GEN10 to compute a sine wave

;ins strt dur  amp(p4)   freq(p5)
i2   0    1    100      880
i2   1.5  1    200      440
i2   3    1    400      220
i2   4.5  1    500     110
i2   6    1    1000     55

;ins strt dur  amp(p4)   freq(p5)  attack(p6)     release(p7)
i3   0    1    10000     440       0.5            0.7
i3   1.5  1    10000     440       0.9            0.1
i3   3    1    5000      880       0.02           0.99
i3   4.5  1    5000      880       0.7            0.01
i3   6    2    20000     220       0.5            0.5

e                     ; indicates the end of the score
</CsScore>
</CsoundSynthesizer>
'''

ret = cs.compileCsdText(csd)
if ret == ctcsound.CSOUND_SUCCESS:
  cs.start()
  cs.perform()
  cs.reset()


