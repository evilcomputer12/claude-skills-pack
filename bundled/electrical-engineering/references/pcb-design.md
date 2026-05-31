# PCB design reference

## Trace width vs. current (IPC-2221)

Use `ee_calc.py trace --i <A> --rise <°C> --thickness <oz>`.

Rule of thumb for **1 oz copper, external, 10 °C rise**:

| Current | ~Width |
|--------:|-------:|
| 0.5 A | ~10 mil |
| 1 A | ~20 mil |
| 2 A | ~40 mil |
| 3 A | ~60 mil |
| 5 A | ~110 mil |

Internal layers carry less (≈half) — they can't shed heat as well. Add margin for connectors,
vias, and long runs. For high current, pour copper and use multiple stitched vias.

## Vias

- A via's current capacity depends on plating; ~0.3–0.5 A per typical 0.3 mm via is conservative.
  **Parallel multiple vias** for power and thermal paths.
- Thermal vias under exposed-pad parts (regulators, MOSFETs) tie heat to inner/bottom copper pours.

## Grounding

- Prefer a **solid ground plane**. Avoid splitting it unless you truly understand the return paths.
- Keep high-speed/return currents tight under their signal traces (the return flows directly
  beneath the trace on the adjacent plane).
- Single-point/star ground only for sensitive mixed-signal; otherwise a continuous plane wins.
- Separate **analog and digital** regions by placement, not by slicing the plane.

## Decoupling placement

- Bypass caps as close to the IC power pin as possible; the via to the plane is part of the loop.
- Smaller packages = lower parasitic inductance. Route pin → cap → ground via with minimal loop area.

## High-speed / signal integrity

- Controlled impedance (e.g. 50 Ω single-ended, 90/100 Ω differential) needs a defined stackup;
  let the fab give you the geometry for your layer count and dielectric.
- Length-match differential pairs and parallel buses where the spec requires.
- Watch stubs, right-angle bends (minor), and reference-plane discontinuities (major).

## EMC basics

- Minimize loop areas (power and signal). Keep switching nodes small.
- Series termination / source resistors slow edges that don't need to be fast.
- Common-mode chokes and TVS on external cables; ground chassis/shield deliberately.
- Guard/keep-out around antennas and switching regulators.

## Manufacturing / DFM

- Honor the fab's min trace/space, drill, annular ring, and soldermask sliver rules.
- Tent or plug vias-in-pad appropriately; specify finish (ENIG for fine-pitch/BGA).
- Add fiducials for assembly, polarity marks, and test points for bring-up.

## KiCad workflow

1. **Schematic:** capture, assign symbols, run ERC, annotate.
2. **Symbol↔footprint:** assign footprints; verify pin mapping against the datasheet.
3. **Netlist → PCB:** import, set up stackup and design rules (from the fab).
4. **Place** by function (group decoupling with its IC, keep switcher loop tight), then **route**.
5. **Pours**, stitching vias, copper balancing.
6. **DRC** clean, then 3D view + BOM + Gerbers/drill + assembly drawings.
7. Cross-check against the fab's capability sheet before ordering.

> If generating schematics programmatically, the **circuit-synth** project can emit KiCad
> schematics from Python — pair it with this skill's calculations and review checklist.
