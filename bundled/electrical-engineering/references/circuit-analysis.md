# Circuit analysis reference

## Fundamental laws

- **Ohm's law:** V = I·R, P = V·I = I²·R = V²/R
- **KCL:** sum of currents into a node = 0.
- **KVL:** sum of voltages around a loop = 0.
- **Series R:** R = R₁ + R₂ + …  Parallel R: 1/R = Σ(1/Rᵢ).  Two in parallel: R₁R₂/(R₁+R₂).
- **Series C:** 1/C = Σ(1/Cᵢ).  Parallel C: C = ΣCᵢ.  (Inductors are the opposite of capacitors.)

## Theorems

- **Thévenin:** any linear two-terminal network = V_th in series with R_th.
  V_th = open-circuit voltage; R_th = V_oc/I_sc (or resistance seen with sources zeroed).
- **Norton:** I_n in parallel with R_n; I_n = I_sc, R_n = R_th.
- **Superposition:** for linear circuits, analyze one independent source at a time
  (zero others: voltage→short, current→open), then sum.
- **Maximum power transfer:** load gets max power when R_load = R_th (only ~50% efficient — not for power supplies).

## Methods

- **Node-voltage:** pick a ground node, write KCL at each remaining node, solve for node voltages.
- **Mesh-current:** assign loop currents, write KVL per mesh, solve.
- Prefer nodal when there are more loops than nodes; mesh when the reverse.

## AC / impedance

- **Capacitor:** Z_C = 1/(jωC), reactance X_C = 1/(2πfC). Current leads voltage 90°.
- **Inductor:** Z_L = jωL, reactance X_L = 2πfL. Voltage leads current 90°.
- **Resonance (series/parallel LC):** f₀ = 1/(2π√(LC)). Q (series RLC) = (1/R)·√(L/C).
- **Impedance magnitude:** |Z| = √(R² + X²); phase φ = atan(X/R).

## Filters (first order)

- **RC low-pass / high-pass:** f_c = 1/(2πRC). Roll-off 20 dB/decade.
- **RL:** f_c = R/(2πL).
- Cascade or use active (Sallen-Key) topologies for steeper roll-off; see components.md for op-amps.

## Transients (first order)

- **Charging:** v(t) = V_final·(1 − e^(−t/τ)). **Discharging:** v(t) = V₀·e^(−t/τ).
- τ = RC (capacitive) or L/R (inductive). ~63% at 1τ, ~99% at 5τ.

## Decibels

- Power: dB = 10·log₁₀(P₂/P₁).  Voltage (same impedance): dB = 20·log₁₀(V₂/V₁).
- dBm = 10·log₁₀(P/1 mW). 0 dBm = 1 mW; +30 dBm = 1 W.
- −3 dB ≈ half power ≈ 0.707× voltage.

## Common gotchas

- Real sources have output impedance — loading changes the voltage.
- Electrolytic/ceramic caps lose capacitance with DC bias and temperature (esp. X5R/X7R).
- Wire/trace resistance and connector drop matter at high current.
- Ground is not a single point — return-current paths cause real voltage differences.
