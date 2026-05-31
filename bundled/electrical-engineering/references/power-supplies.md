# Power supply design reference

## Choosing a topology

| Need | Use |
|------|-----|
| Small step-down, low noise, low current (<~300 mA), V_in close to V_out | **LDO** |
| Efficient step-down, higher current, larger V_in−V_out gap | **Buck** |
| Step-up (V_out > V_in) | **Boost** |
| Step up/down (battery crossing V_out) | **Buck-boost / SEPIC** |
| Isolation / mains | **Isolated DC-DC / certified AC-DC module** |

## LDO essentials

- **Dropout:** V_in must exceed V_out by the dropout voltage at max load.
- **Power dissipated = (V_in − V_out) · I_load** → all becomes heat. Check θ_JA and ambient:
  ΔT = P · θ_JA. Add copper/heatsink or switch to a buck if too hot.
- Input/output caps per datasheet (often low-ESR ceramic); some LDOs need a minimum ESR — check.
- Good for analog rails after a switcher (post-regulation for low noise).

## Switching (buck) essentials

- Inductor: choose for ripple ΔI_L ≈ 20–40% of I_out; verify **I_sat > I_peak**.
- Output cap: ripple = ΔI_L/(8·f·C_out) (+ ESR term). Use low-ESR ceramics/polymer.
- Input cap: handles pulsed input current — place close to the IC; size RMS ripple current.
- **Layout is the design:** keep the hot loop (input cap → switch → diode/synch FET) tiny;
  short, wide power traces; solid ground; sense/feedback away from the inductor node.
- Set V_out via feedback divider (datasheet V_FB); use ±1% resistors.

## Decoupling / bypass

- One **0.1 µF** ceramic per IC power pin, placed right at the pin; add **1–10 µF** bulk per rail
  per region; add board-level bulk near the regulator.
- For fast digital, smaller package = lower inductance; multiple values can help but watch
  anti-resonance. Keep the cap→pin→ground loop short.

## Bulk capacitance / hold-up

- For a load step or hold-up time t: C ≈ I·t / ΔV (allowed droop).
- Account for ESR: instantaneous droop = I·ESR.

## Thermal

- Junction temp T_J = T_ambient + P · θ_JA. Stay well below the rating (e.g. ≤105–125 °C with margin).
- Copper pour, thermal vias under exposed pads, and airflow all reduce θ_JA.

## Batteries

- **Runtime ≈ capacity (Ah) · derate / average current (A)** — derate for temperature, cutoff,
  and aging (0.7–0.8 typical).
- Li-ion/LiPo: never over-charge/over-discharge; use a protected pack + proper charger IC;
  respect charge current and temperature window. Treat as a safety item.
- Add reverse-polarity protection (series Schottky or ideal-diode/P-FET) and fusing.

## Protection checklist

- Reverse polarity, over-voltage (TVS), over-current (fuse/PTC), inrush limiting (NTC/soft-start),
  ESD on external connectors, and a bleeder where caps hold charge.

## Bench verification

- Check V_out at min/max load and line; measure ripple with a **short ground-spring probe**
  (not a long clip — it picks up switching noise), load-step transient, and thermal rise after soak.
