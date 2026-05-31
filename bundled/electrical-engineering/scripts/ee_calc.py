#!/usr/bin/env python3
"""Electrical-engineering calculators. No external dependencies. ASCII-only output.

Values accept SI suffixes: k, M(=1e6), G, m, u, n, p.
Run `python ee_calc.py <command> --help` for per-command options.
"""
import argparse
import math
import sys

_SUFFIX = {
    'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'µ': 1e-6, 'm': 1e-3,
    'k': 1e3, 'K': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12,
}

E_SERIES = {
    'E6':  [10, 15, 22, 33, 47, 68],
    'E12': [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82],
    'E24': [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36,
            39, 43, 47, 51, 56, 62, 68, 75, 82, 91],
    'E96': [round(10 ** (i / 96), 2) for i in range(96)],
}


def si(s):
    """Parse a number that may carry an SI suffix, e.g. '4.7k' or '4700'."""
    if s is None:
        return None
    s = str(s).strip().replace('Ω', '').replace('ohm', '').replace('F', '').replace('H', '')
    if not s:
        raise ValueError('empty value')
    if s[-1] in _SUFFIX:
        return float(s[:-1]) * _SUFFIX[s[-1]]
    return float(s)


def fmt(value, unit=''):
    """Format a value with an engineering SI prefix (ASCII 'u' for micro)."""
    if value == 0:
        return f'0 {unit}'.strip()
    neg = value < 0
    value = abs(value)
    prefixes = [(1e12, 'T'), (1e9, 'G'), (1e6, 'M'), (1e3, 'k'),
                (1, ''), (1e-3, 'm'), (1e-6, 'u'), (1e-9, 'n'), (1e-12, 'p')]
    for scale, pre in prefixes:
        if value >= scale:
            out = f'{value / scale:.4g} {pre}{unit}'.strip()
            return ('-' + out) if neg else out
    out = f'{value:.4g} {unit}'.strip()
    return ('-' + out) if neg else out


def nearest_eseries(value, series):
    """Snap a positive value to the nearest preferred value in an E-series.

    Tables are stored in different ranges (E24 as 10..91, E96 as 1.0..9.77),
    so normalize every base value into [1, 10) before comparing.
    """
    if value <= 0:
        return value
    norm_base = []
    for b in E_SERIES[series]:
        x = float(b)
        while x >= 10:
            x /= 10
        while x < 1:
            x *= 10
        norm_base.append(x)
    norm_base = sorted(set(norm_base)) + [10.0]
    decade = 10 ** math.floor(math.log10(value))
    norm = value / decade                       # in [1, 10)
    best = min(norm_base, key=lambda b: abs(b - norm))
    return best * decade


# --- commands ---------------------------------------------------------------

def cmd_ohm(a):
    """Ohm's law: provide any two of V, I, R; get the rest + power."""
    V, I, R = a.v, a.i, a.r
    if sum(x is not None for x in (V, I, R)) < 2:
        sys.exit("ohm: provide at least two of --v, --i, --r")
    if V is None:
        V = I * R
    elif I is None:
        I = V / R
    elif R is None:
        R = V / I
    print(f"V = {fmt(V, 'V')}")
    print(f"I = {fmt(I, 'A')}")
    print(f"R = {fmt(R, 'ohm')}")
    print(f"P = {fmt(V * I, 'W')}")


def cmd_divider(a):
    """Resistive voltage divider: Vout = Vin * R2/(R1+R2)."""
    vout = a.vin * a.r2 / (a.r1 + a.r2)
    iq = a.vin / (a.r1 + a.r2)
    print(f"Vout = {fmt(vout, 'V')}")
    print(f"Divider current = {fmt(iq, 'A')}  (power in R1 = {fmt(iq**2*a.r1, 'W')})")
    print("Note: keep divider current >> load current, or buffer with an op-amp.")


def cmd_led(a):
    """Series resistor for an LED."""
    if a.i <= 0:
        sys.exit("led: --i must be > 0")
    r = (a.vsupply - a.vf) / a.i
    near = nearest_eseries(r, 'E24')
    print(f"Required resistor = {fmt(r, 'ohm')}")
    print(f"Nearest E24 = {fmt(near, 'ohm')}  -> I = {fmt((a.vsupply-a.vf)/near, 'A')}")
    print(f"Resistor power = {fmt((a.vsupply-a.vf)*a.i, 'W')}  (use a part rated >= 2x)")


def cmd_rc(a):
    """RC time constant and -3 dB cutoff."""
    tau = a.r * a.c
    fc = 1 / (2 * math.pi * a.r * a.c)
    print(f"tau = {fmt(tau, 's')}")
    print(f"5*tau (settle) = {fmt(5 * tau, 's')}")
    print(f"f_-3dB = {fmt(fc, 'Hz')}")


def cmd_lc(a):
    """LC resonant frequency."""
    f = 1 / (2 * math.pi * math.sqrt(a.l * a.c))
    z = math.sqrt(a.l / a.c)
    print(f"f_resonant = {fmt(f, 'Hz')}")
    print(f"Characteristic impedance = {fmt(z, 'ohm')}")


def cmd_parallel(a):
    """Parallel resistance of N resistors."""
    vals = [si(v) for v in a.values]
    rp = 1 / sum(1 / v for v in vals)
    print(f"R_parallel = {fmt(rp, 'ohm')}")


def cmd_series(a):
    """Series resistance / sum."""
    vals = [si(v) for v in a.values]
    print(f"R_series = {fmt(sum(vals), 'ohm')}")


def cmd_power(a):
    """Power dissipation P = V*I (or specify R with one of V/I)."""
    if a.v is not None and a.i is not None:
        p = a.v * a.i
    elif a.v is not None and a.r is not None:
        p = a.v ** 2 / a.r
    elif a.i is not None and a.r is not None:
        p = a.i ** 2 * a.r
    else:
        sys.exit("power: give --v & --i, or --v & --r, or --i & --r")
    print(f"P = {fmt(p, 'W')}")


def cmd_trace(a):
    """PCB trace width from IPC-2221 (external layer by default)."""
    # IPC-2221: I = k * dT^0.44 * A^0.725 ; A in mils^2, dT in degC, I in A
    k = 0.024 if a.internal else 0.048
    area_mils2 = (a.i / (k * a.rise ** 0.44)) ** (1 / 0.725)
    width_mils = area_mils2 / (a.thickness * 1.378)   # 1 oz copper = 1.378 mil thick
    layer = "internal" if a.internal else "external"
    print(f"Trace ({layer}, {a.thickness} oz, dT={a.rise} degC, I={a.i} A):")
    print(f"  cross-section = {area_mils2:.1f} mil^2")
    print(f"  width = {width_mils:.1f} mil  ({width_mils * 0.0254:.3f} mm)")
    print("  (IPC-2221; add margin for vias, connectors, and long runs.)")


def cmd_555(a):
    """555 astable frequency and duty cycle."""
    f = 1.44 / ((a.r1 + 2 * a.r2) * a.c)
    duty = (a.r1 + a.r2) / (a.r1 + 2 * a.r2) * 100
    t_high = 0.693 * (a.r1 + a.r2) * a.c
    t_low = 0.693 * a.r2 * a.c
    print(f"f = {fmt(f, 'Hz')}")
    print(f"duty = {duty:.1f}%   (t_high={fmt(t_high, 's')}, t_low={fmt(t_low, 's')})")


def cmd_reactance(a):
    """Capacitive / inductive reactance at a frequency."""
    if a.c is None and a.l is None:
        sys.exit("reactance: provide --c and/or --l")
    if a.c is not None:
        print(f"Xc = {fmt(1 / (2 * math.pi * a.f * a.c), 'ohm')}")
    if a.l is not None:
        print(f"Xl = {fmt(2 * math.pi * a.f * a.l, 'ohm')}")


def cmd_eseries(a):
    """Snap a value to the nearest E-series preferred value."""
    near = nearest_eseries(a.value, a.series)
    err = (near - a.value) / a.value * 100
    print(f"{a.series} nearest to {fmt(a.value)} = {fmt(near)}  ({err:+.1f}%)")


def cmd_dbm(a):
    """Convert between dBm and watts."""
    if a.dbm is None and a.watt is None:
        sys.exit("dbm: provide --dbm or --watt")
    if a.dbm is not None:
        print(f"{a.dbm} dBm = {fmt(10 ** (a.dbm / 10) / 1000, 'W')}")
    if a.watt is not None:
        print(f"{fmt(a.watt, 'W')} = {10 * math.log10(a.watt * 1000):.2f} dBm")


# --- argparse wiring --------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    val = si  # SI-aware argument type

    s = sub.add_parser('ohm', help="Ohm's law (any 2 of V/I/R)")
    s.add_argument('--v', type=val); s.add_argument('--i', type=val); s.add_argument('--r', type=val)
    s.set_defaults(func=cmd_ohm)

    s = sub.add_parser('divider', help='resistive voltage divider')
    s.add_argument('--vin', type=val, required=True)
    s.add_argument('--r1', type=val, required=True)
    s.add_argument('--r2', type=val, required=True)
    s.set_defaults(func=cmd_divider)

    s = sub.add_parser('led', help='LED series resistor')
    s.add_argument('--vsupply', type=val, required=True)
    s.add_argument('--vf', type=val, required=True, help='LED forward voltage')
    s.add_argument('--i', type=val, required=True, help='target current')
    s.set_defaults(func=cmd_led)

    s = sub.add_parser('rc', help='RC time constant + cutoff')
    s.add_argument('--r', type=val, required=True); s.add_argument('--c', type=val, required=True)
    s.set_defaults(func=cmd_rc)

    s = sub.add_parser('lc', help='LC resonant frequency')
    s.add_argument('--l', type=val, required=True); s.add_argument('--c', type=val, required=True)
    s.set_defaults(func=cmd_lc)

    s = sub.add_parser('parallel', help='parallel resistors')
    s.add_argument('values', nargs='+'); s.set_defaults(func=cmd_parallel)

    s = sub.add_parser('series', help='series resistors')
    s.add_argument('values', nargs='+'); s.set_defaults(func=cmd_series)

    s = sub.add_parser('power', help='power dissipation')
    s.add_argument('--v', type=val); s.add_argument('--i', type=val); s.add_argument('--r', type=val)
    s.set_defaults(func=cmd_power)

    s = sub.add_parser('trace', help='PCB trace width (IPC-2221)')
    s.add_argument('--i', type=val, required=True, help='current (A)')
    s.add_argument('--rise', type=float, default=10, help='allowed temp rise degC (default 10)')
    s.add_argument('--thickness', type=float, default=1.0, help='copper weight in oz (default 1)')
    s.add_argument('--internal', action='store_true', help='internal layer')
    s.set_defaults(func=cmd_trace)

    s = sub.add_parser('555', help='555 astable')
    s.add_argument('--r1', type=val, required=True); s.add_argument('--r2', type=val, required=True)
    s.add_argument('--c', type=val, required=True); s.set_defaults(func=cmd_555)

    s = sub.add_parser('reactance', help='Xc / Xl at frequency')
    s.add_argument('--f', type=val, required=True)
    s.add_argument('--c', type=val); s.add_argument('--l', type=val)
    s.set_defaults(func=cmd_reactance)

    s = sub.add_parser('eseries', help='snap to E-series')
    s.add_argument('--value', type=val, required=True)
    s.add_argument('--series', choices=list(E_SERIES), default='E24')
    s.set_defaults(func=cmd_eseries)

    s = sub.add_parser('dbm', help='dBm <-> watts')
    s.add_argument('--dbm', type=float); s.add_argument('--watt', type=val)
    s.set_defaults(func=cmd_dbm)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
