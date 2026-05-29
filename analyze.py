#!/usr/bin/env python3
# Verify key Twenty-Seven-Windows numbers from the real 2000 zeros, and
# emit clean series for the SVG charts. Numbers from files only.
import numpy as np, json

g = np.array([float(x) for x in open("riemann_zeros_2000.txt") if x.strip()])
N = len(g)

# --- Smooth zero-counting function N_smooth(t) = (t/2pi) log(t/2pi) - t/2pi + 7/8
def Nsmooth(t):
    x = t/(2*np.pi)
    return x*np.log(x) - x + 7.0/8.0

# S(t): the "wind" = actual count minus smooth, evaluated just above each zero.
# Actual count at gamma_n (counting from 1) ~ n - 0.5 at the zero; use index.
n_idx = np.arange(1, N+1)
S = (n_idx - 0.5) - Nsmooth(g)            # tremor of the count around its trend
std_S = S.std()

# Window 05 bands: std(S)/v ratio falling with spin velocity v = 0.5 log(t/2pi)
def vspin(t): return 0.5*np.log(t/(2*np.pi))
bands = [(14,396),(682,939),(1185,1419),(1872,2090),(2306,2515)]
band_rows=[]
for lo,hi in bands:
    m=(g>=lo)&(g<=hi)
    v=vspin(g[m]).mean(); s=S[m].std()
    band_rows.append((lo,hi,round(v,3),round(s,3),round(s/v,3)))

# Spacings (unfolded) for repulsion / smallest gap
dens = np.gradient(Nsmooth(g))            # local spacing of smooth count ~ d N/dn
gaps = np.diff(g)
unfold = gaps * 0.5*np.log(g[:-1]/(2*np.pi))  # unfolded gaps ~ mean 1
lag1 = np.corrcoef(unfold[:-1], unfold[1:])[0,1]
min_gap = gaps.min()

# Prime-wave correlation (Window 04): reconstruct S from primes p<=P
def primes_upto(n):
    sieve=np.ones(n+1,bool); sieve[:2]=False
    for i in range(2,int(n**0.5)+1):
        if sieve[i]: sieve[i*i::i]=False
    return np.nonzero(sieve)[0]
P=primes_upto(1000)
# prime wave: -2 sum_p sum_k (log p / p^{k/2}) cos(gamma * k log p)/ ... (schematic, bounded)
def primewave(t):
    s=np.zeros_like(t)
    for p in P:
        lp=np.log(p)
        for k in (1,2):
            s += -2*(lp/ p**(k/2.0))*np.cos(t*k*lp)/(k)  # bounded proxy of the oscillating term
    return s
pw = primewave(g)
# align scale (both are oscillatory mean-zero); correlation of shapes
corr_pw = np.corrcoef(pw - pw.mean(), S - S.mean())[0,1]

summary = {
 "N": N,
 "first": float(g[0]), "last": float(g[-1]),
 "std_S": round(float(std_S),4),
 "spiral_lag1": round(float(lag1),3),
 "min_gap": round(float(min_gap),3),
 "corr_primewave_S": round(float(corr_pw),3),
 "bands": band_rows,
}
print(json.dumps(summary, indent=1))

# Emit downsampled series for SVG (every k-th point to keep files light)
def dump(name, x, y, k=1):
    xs=x[::k]; ys=y[::k]
    json.dump({"x":[round(float(a),4) for a in xs],
               "y":[round(float(b),5) for b in ys]}, open(name,"w"))
dump("series_wind.json", g, S, k=1)
dump("series_gaps.json", g[:-1], unfold, k=1)
print(">>> series written")
