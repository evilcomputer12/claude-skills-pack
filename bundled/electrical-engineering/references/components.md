# Component selection reference

## E-series preferred values

Use these standard values instead of arbitrary numbers (snap with `ee_calc.py eseries`):

- **E6** (±20%): 10 15 22 33 47 68
- **E12** (±10%): 10 12 15 18 22 27 33 39 47 56 68 82
- **E24** (±5%): adds 11 13 16 20 24 30 36 43 51 62 75 91
- **E96** (±1%): 96 values per decade — for precision dividers, references.

## Resistors

- Spec: value, tolerance, **power rating**, package, temperature coefficient (ppm/°C).
- Derate power ≥2×. SMD: 0402≈1/16 W, 0603≈1/10 W, 0805≈1/8 W, 1206≈1/4 W (board/temp dependent).
- For dividers feeding ADCs/references, use ±1% (E96) and matched tempco.
- High value (>1 MΩ) → noise & leakage sensitivity; low value → wasted current.

## Capacitors (pick by dielectric)

- **Ceramic C0G/NP0:** stable, low value, great for filters/timing/RF.
- **Ceramic X7R/X5R:** bulk/decoupling; **loses capacitance with DC bias & temp** — derate generously
  (a 10 µF 0603 at rated voltage may deliver <5 µF).
- **Electrolytic / aluminum polymer:** bulk energy storage; watch ESR, ripple-current rating,
  lifetime (Arrhenius: hotter = shorter), and **voltage derate ≥50%**.
- **Film:** stable, high voltage, low ESR; snubbers, audio, mains.
- **Tantalum:** dense but fails short — derate voltage ≥50% and avoid surge without limiting.

## Inductors

- Spec: inductance, **saturation current (I_sat)**, RMS current rating, DCR, SRF.
- For switchers, keep ripple current within I_sat with margin; DCR adds loss.

## Diodes

- **Standard rectifier:** ~0.7 V drop. **Schottky:** ~0.3–0.4 V, fast, low V_R — reverse polarity,
  freewheel, OR-ing. **Zener:** voltage reference/clamp. **TVS:** transient/ESD protection.
- Spec: V_R (reverse), I_F (forward), reverse recovery (t_rr) for switching.

## BJT vs. MOSFET (switching)

- **BJT:** current-controlled; V_CE(sat) drop; fine for small signal/low power.
- **MOSFET:** voltage-controlled gate; choose by **R_DS(on)**, V_GS(th), V_DS rating (derate ≥50%),
  gate charge (Q_g) for switching speed, SOA, package thermal.
- **N-channel low-side** is easiest; **P-channel or high-side driver** for high-side switching.
- Always: gate resistor, gate pull-down (so it's off at power-up), and flyback/TVS for inductive loads.

## Op-amps

- Key specs: supply range (single vs. dual), **rail-to-rail** in/out, input bias current,
  offset voltage, GBW (gain-bandwidth), slew rate, noise.
- Topologies: non-inverting (gain = 1+Rf/Rg), inverting (−Rf/Rin), buffer (unity), difference,
  integrator/differentiator, Sallen-Key filters.
- Watch stability with capacitive loads; add feedback compensation or isolation resistor.

## Voltage references

- For ADCs/precision: use a dedicated reference IC (series or shunt), not a divider.
- Spec: initial accuracy, tempco (ppm/°C), noise, load/line regulation.

## Crystals / oscillators

- Crystal needs correct load capacitance (C_L) → choose load caps: C ≈ 2·(C_L − C_stray).
- For MCUs, a packaged oscillator avoids tuning if you have margin in the BOM.

## Connectors & protection

- Rate connectors for current + mating cycles; add ESD/TVS on external I/O.
- Series resistors on long digital lines; common-mode chokes on USB/Ethernet/CAN.
