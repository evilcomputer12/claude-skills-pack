# SPICE simulation reference (ngspice)

Simulate before you solder. ngspice is free and scriptable. KiCad embeds it for schematic-driven sim.

## Netlist anatomy

```spice
* Title line is REQUIRED (first line is treated as a comment/title)
.title RC low-pass

* Elements: <name> <node+> <node-> <value>
V1 in 0 DC 0 AC 1 SIN(0 1 1k)   ; source: DC, AC mag, transient SIN(offset amp freq)
R1 in out 1k
C1 out 0 100n

.end
```

- Node `0` is always ground.
- Suffixes: f p n u m k meg g t  (note: **meg** = 1e6, `m` = milli — `1Meg` ≠ `1m`).

## DC operating point & sweep

```spice
.op                      ; one operating point
.dc V1 0 5 0.1           ; sweep V1 from 0 to 5 V in 0.1 V steps
```

## AC analysis (frequency response)

```spice
.ac dec 100 1 1Meg       ; 100 points/decade, 1 Hz to 1 MHz
* plot: vdb(out) for magnitude in dB, vp(out) for phase
```

## Transient

```spice
.tran 1u 5m             ; step 1 µs, stop 5 ms
* plot v(out) v(in)
```

## Example: RC low-pass Bode

```spice
.title RC LPF
V1 in 0 AC 1
R1 in out 1k
C1 out 0 100n
.ac dec 200 10 1Meg
.control
run
plot vdb(out)
.endc
.end
```

Cutoff should land at f_c = 1/(2πRC) ≈ 1.59 kHz — cross-check with `ee_calc.py rc --r 1k --c 100n`.

## Models & subcircuits

```spice
.model MyDiode D(IS=1e-14 N=1.8 RS=0.1)
D1 a b MyDiode

.include opamp.lib       ; vendor SPICE model
X1 in+ in- vcc vee out OPAMP_PART   ; subcircuit instance
```

Grab manufacturer SPICE models from the part's product page; generic models hide real behavior.

## Worst-case / Monte Carlo

- Sweep temperature: `.temp 0 25 85` (or `.step temp ...`).
- Tolerances: `.step` parameters, or Monte Carlo via `.control` loops with `gauss()`/`unif()`.
- Always check: startup, load step, line step, and over temperature — not just nominal.

## .control scripting

```spice
.control
  run
  meas tran vpp PP v(out)        ; measure peak-to-peak
  meas ac fc when vdb(out)=-3    ; find -3 dB frequency
  print vpp fc
.endc
```

## Limits

SPICE is only as good as its models and your netlist. It won't catch layout parasitics, EMC,
thermal coupling, or mechanical issues — use it to validate topology and values, then verify on the bench.
