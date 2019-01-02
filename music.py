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

#ENVELOPE
# kr linen kamp, irise, idur, idec
# ar linen xamp, irise, idur, idec

# The output of the linen (k1) is patched into the kamp argument of an oscil. 
# This applies an envelope to the oscil. The orchestra and score files now appear as:

#VIBRATO 
# kr linseg ia, idur1, ib[, idur2, ic[...]]
# ar linseg ia, idur1, ib[, idur2, ic[...]]



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
a1        oscil     p4, p5, 1           ; p4=amp
          out       a1                  ; p5=freq
          endin

          instr 3                       ; p3=duration of note
k1        linen     p4, p6, p3, p7      ; p4=amp
a1        oscil     k1, p5, 1           ; p5=freq
          out       a1                  ; p6=attack time
          endin                         ; p7=release time

                    instr 4
iamp      =         ampdb(p4)           ; convert decibels to linear amp
iscale    =         iamp * .333         ; scale the amp at initialization
inote     =         cpspch(p5)          ; convert octave.pitch to cps

k1        linen     iscale, p6, p3, p7  ; p4=amp

a3        oscil     k1, inote*.996, 1   ; p5=freq
a2        oscil     k1, inote*1.004, 1  ; p6=attack time
a1        oscil     k1, inote, 1        ; p7=release time

a1        =         a1+a2+a3
          out       a1
          endin

                    instr 5
irel      =         0.01                               ; set vibrato release time
idel1     =         p3 * p10                           ; calculate initial delay (% of dur)
isus      =         p3 - (idel1 + irel)                ; calculate remaining duration

iamp      =         ampdb(p4)
iscale    =         iamp * .333                        ; p4=amp
inote     =         cpspch(p5)                         ; p5=freq

k3        linseg    0, idel1, p9, isus, p9, irel, 0    ; p6=attack time
k2        oscil     k3, p8, 1                          ; p7=release time
k1        linen     iscale, p6, p3, p7                 ; p8=vib rate

a3        oscil     k1, inote*.995+k2, 1               ; p9=vib depth
a2        oscil     k1, inote*1.005+k2, 1              ; p10=vib delay (0-1)
a1        oscil     k1, inote+k2, 1

          out       a1+a2+a3
          endin



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

;ins strt dur  amp  freq      attack    release
i4   0    1    75   8.04      0.1       0.7
i4   1    1    70   8.02      0.07      0.6
i4   2    1    75   8.00      0.05      0.5
i4   3    1    70   8.02      0.05      0.4
i4   4    1    85   8.04      0.1       0.5
i4   5    1    80   8.04      0.05      0.5
i4   6    2    90   8.04      0.03      1.

;ins strt dur  amp  freq      atk  rel  vibrt     vbdpt     vbdel
i5   0    3    86   10.00     0.1  0.7  7         6         .4
i5   4    3    86   10.02     1    0s.2  6         6         .4
i5   8    4    86   10.04     2    1    5         6    



e                     ; indicates the end of the score
</CsScore>
</CsoundSynthesizer>
'''

ret = cs.compileCsdText(csd)
if ret == ctcsound.CSOUND_SUCCESS:
  cs.start()
  cs.perform()
  cs.reset()


