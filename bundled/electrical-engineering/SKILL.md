---
name: electrical-engineering
description: Electrical and electronics engineering assistant for circuit analysis, component selection, power supply design, analog/digital design, PCB layout, SPICE simulation, and embedded hardware. Use when designing or debugging circuits, choosing components (resistors, capacitors, MOSFETs, regulators, op-amps), sizing power supplies, computing values (Ohm's law, dividers, RC/LC, filters, LED resistors, PCB trace width), reviewing schematics/netlists, or working with KiCad, SPICE/ngspice, or microcontroller hardware.
license: MIT
---

# Electrical Engineering

A practical toolkit for analog, digital, power, and embedded hardware work — from
back-of-envelope calculations to schematic review and PCB layout sanity checks.

## When to use this skill

Trigger for any of:

- **Circuit analysis** — DC/AC, Ohm's & Kirchhoff's laws, Thévenin/Norton, node/mesh, transients.
- **Component selection** — resistors, capacitors, inductors, diodes, BJTs/MOSFETs, op-amps,
  voltage regulators (LDO vs. buck/boost), connectors, crystals.
- **Power** — supply sizing, regulator choice, thermal/power dissipation, battery runtime,
  decoupling, bulk capacitance, efficiency.
- **Analog design** — filters (RC/LC, active), op-amp circuits, amplifiers, references, ADC/DAC front-ends.
- **Digital / embedded** — logic levels, level shifting, pull-ups, debouncing, I²C/SPI/UART wiring,
  GPIO current limits, microcontroller power and reset.
- **PCB layout** — trace width vs. current (IPC-2221), via sizing, grounding, decoupling placement,
  impedance, EMC basics.
- **Simulation & tools** — SPICE/ngspice netlists, KiCad workflow, measurement/debug strategy.

## Workflow

1. **Clarify the spec.** Voltages, currents, frequency, tolerance, temperature, budget, form
   factor, safety/regulatory constraints. State assumptions explicitly when the user doesn't.
2. **Do the math first.** Use `scripts/ee_calc.py` for common closed-form calculations before
   recommending parts — show the numbers and the formula used.
3. **Pick from E-series and real parts.** Snap resistor/cap values to E12/E24/E96; prefer common,
   in-production parts and standard packages. Note availability when it matters.
4. **Check the margins.** Power dissipation vs. package rating, voltage/current derating
   (≥50% derating for electrolytics & MOSFET V_DS is a good default), worst-case tolerance stack-up,
   thermal rise.
5. **Sanity-check, then simulate.** For non-trivial analog/power, write a SPICE netlist
   (see `references/spice-simulation.md`) rather than trusting intuition.
6. **Document.** Give the chosen values, the reasoning, and what to verify on the bench.

## Quick calculators

Run the helper for instant, formula-backed numbers:

```bash
python scripts/ee_calc.py ohm --v 5 --r 220          # current through a resistor
python scripts/ee_calc.py divider --vin 12 --r1 10k --r2 3.3k
python scripts/ee_calc.py led --vsupply 5 --vf 2.1 --i 10m
python scripts/ee_calc.py rc --r 10k --c 100n         # time constant + cutoff freq
python scripts/ee_calc.py lc --l 10u --c 100n         # resonant frequency
python scripts/ee_calc.py parallel 10k 22k 47k        # parallel resistance
python scripts/ee_calc.py power --v 3.3 --i 500m       # power dissipation
python scripts/ee_calc.py trace --i 2 --rise 10        # PCB trace width (IPC-2221)
python scripts/ee_calc.py 555 --r1 10k --r2 47k --c 1u # astable freq/duty
python scripts/ee_calc.py reactance --f 1k --c 100n    # capacitive reactance
python scripts/ee_calc.py eseries --value 3300 --series E24
```

Run `python scripts/ee_calc.py --help` (or `<cmd> --help`) for all options. Values accept
SI suffixes: `k`, `M`, `m`, `u`/`µ`, `n`, `p`.

## Reference material

Load only what's relevant to the task:

- **`references/circuit-analysis.md`** — laws, theorems, AC impedance, transients, decibels.
- **`references/components.md`** — choosing R/C/L, diodes, BJT/MOSFET, op-amps; E-series; packages.
- **`references/power-supplies.md`** — LDO vs. switching, sizing, decoupling, thermal, batteries.
- **`references/pcb-design.md`** — trace width, vias, grounding, decoupling, impedance, EMC, KiCad.
- **`references/spice-simulation.md`** — ngspice netlist patterns for DC/AC/transient/Monte-Carlo.

## Guardrails

- **Mains / high voltage (>50 V) and battery safety are dangerous.** Give correct guidance
  (isolation, creepage/clearance, fusing, protection) but remind the user to follow local
  electrical code and, for mains products, use certified modules and proper review. Do not
  hand-wave safety-critical design.
- Always show the **formula and the worst-case**, not just a nominal value.
- Prefer **standard E-series values and real, available parts** over exact ideal numbers.
- When unsure of a manufacturer-specific spec, say so and point to the datasheet parameter to check.

## Optional companion tool

If the project uses **circuit-synth** (a Python library that generates KiCad schematics from
code), this skill's analysis/calculations pair well with it — but circuit-synth is a separate
project, not required by this skill.
