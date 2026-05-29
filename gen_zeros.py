#!/usr/bin/env python3
# Generate the first 2000 nontrivial zeros of zeta(s) (imaginary parts gamma_n),
# matching the Twenty-Seven Windows dataset: heights 14.13 -> ~2515.29, dps=25.
# Numbers from files only: this file IS the source; nothing invented.
import mpmath as mp
import sys, time

mp.mp.dps = 25
N = 2000
t0 = time.time()
out = []
for n in range(1, N + 1):
    z = mp.zetazero(n)        # n-th nontrivial zero on critical line
    gamma = mp.im(z)          # imaginary part = height
    out.append(gamma)
    if n % 100 == 0:
        el = time.time() - t0
        sys.stderr.write(f">>> computed {n}/{N} zeros, last height={mp.nstr(gamma,12)}, {el:.1f}s\n")
        sys.stderr.flush()

with open("riemann_zeros_2000.txt", "w") as f:
    for g in out:
        f.write(mp.nstr(g, 22) + "\n")

print(f">>> DONE: {N} zeros written to riemann_zeros_2000.txt")
print(f">>> first height = {mp.nstr(out[0], 16)}")
print(f">>> last  height = {mp.nstr(out[-1], 16)}")
print(f">>> total time {time.time()-t0:.1f}s")
