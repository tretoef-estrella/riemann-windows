#!/usr/bin/env python3
# Build four clean SVG charts (Quanta-ish: warm paper, dark ink, one accent).
# Every datum traces to verified numbers in analyze.py output. Nothing invented.
import json, numpy as np

PAPER="#faf6ef"; INK="#1a1a1a"; MUT="#6b6ب".replace("ب","b"); ACC="#c0392b"; ACC2="#2c6e8f"
MUT="#7a7367"
W,H=820,420; ML,MR,MT,MB=70,30,46,56
PW,PH=W-ML-MR,H-MT-MB

def frame(title, sub):
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Georgia, \'Times New Roman\', serif">']
    s.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>')
    s.append(f'<text x="{ML}" y="26" font-size="19" fill="{INK}" font-weight="bold">{title}</text>')
    s.append(f'<text x="{ML}" y="42" font-size="12.5" fill="{MUT}">{sub}</text>')
    return s

def axes(s, x0,x1,y0,y1, xlab,ylab, yticks):
    def X(v): return ML+(v-x0)/(x1-x0)*PW
    def Y(v): return MT+PH-(v-y0)/(y1-y0)*PH
    s.append(f'<line x1="{ML}" y1="{MT+PH}" x2="{ML+PW}" y2="{MT+PH}" stroke="{INK}" stroke-width="1.1"/>')
    s.append(f'<line x1="{ML}" y1="{MT}" x2="{ML}" y2="{MT+PH}" stroke="{INK}" stroke-width="1.1"/>')
    for yt in yticks:
        yy=Y(yt)
        s.append(f'<line x1="{ML-4}" y1="{yy:.1f}" x2="{ML}" y2="{yy:.1f}" stroke="{INK}"/>')
        s.append(f'<line x1="{ML}" y1="{yy:.1f}" x2="{ML+PW}" y2="{yy:.1f}" stroke="{MUT}" stroke-opacity="0.18"/>')
        s.append(f'<text x="{ML-9}" y="{yy+4:.1f}" font-size="11" fill="{MUT}" text-anchor="end">{yt:g}</text>')
    s.append(f'<text x="{ML+PW/2}" y="{H-14}" font-size="12.5" fill="{MUT}" text-anchor="middle">{xlab}</text>')
    s.append(f'<text x="18" y="{MT+PH/2}" font-size="12.5" fill="{MUT}" text-anchor="middle" transform="rotate(-90 18 {MT+PH/2})">{ylab}</text>')
    return X,Y

# ---------- Chart 1: The Wind S(t) ----------
w=json.load(open("series_wind.json")); x=np.array(w["x"]); y=np.array(w["y"])
s=frame("The Wind — S(t)", "The tremor of the zero-count around its smooth trend · 2000 real zeros · std = 0.2691")
X,Y=axes(s, x.min(), x.max(), -0.85, 0.85, "height  t  (14 → 2515)", "S(t)", [-0.8,-0.4,0,0.4,0.8])
s.append(f'<line x1="{ML}" y1="{Y(0):.1f}" x2="{ML+PW}" y2="{Y(0):.1f}" stroke="{INK}" stroke-opacity="0.35" stroke-dasharray="3 3"/>')
pts=" ".join(f"{X(a):.1f},{Y(b):.1f}" for a,b in zip(x,y))
s.append(f'<polyline points="{pts}" fill="none" stroke="{ACC2}" stroke-width="0.8" stroke-opacity="0.9"/>')
s.append('</svg>')
open("chart_wind.svg","w").write("\n".join(s))

# ---------- Chart 2: Spiral tremor memory (lag-1 scatter) ----------
gg=json.load(open("series_gaps.json")); u=np.array(gg["y"])
a=u[:-1]-u[:-1].mean(); b=u[1:]-u[1:].mean()
s=frame("The Swing — memory in the turn", "Each unfolded gap vs the next · lag-1 autocorrelation = −0.39 (repulsion seen from the phase)")
X,Y=axes(s, -1.2,1.6, -1.2,1.6, "gap n  (centered)", "gap n+1  (centered)", [-1,0,1])
# trend line (negative slope)
import numpy as _np
slope=_np.polyfit(a,b,1)[0]; inter=_np.polyfit(a,b,1)[1]
s.append(f'<line x1="{X(-1.2):.1f}" y1="{Y(slope*-1.2+inter):.1f}" x2="{X(1.6):.1f}" y2="{Y(slope*1.6+inter):.1f}" stroke="{ACC}" stroke-width="2"/>')
for ai,bi in zip(a[::1],b[::1]):
    s.append(f'<circle cx="{X(ai):.1f}" cy="{Y(bi):.1f}" r="1.3" fill="{INK}" fill-opacity="0.33"/>')
s.append('</svg>')
open("chart_swing.svg","w").write("\n".join(s))

# ---------- Chart 3: Speed steadies the line (Window 05 bands) ----------
bands=[(1.718,0.134),(2.428,0.107),(2.666,0.103),(2.876,0.097),(2.975,0.095)]
s=frame("Speed Steadies the Line", "Relative tremor std(S)/v falls as the spiral spins faster · corr = −0.99")
X,Y=axes(s, 1.6,3.05, 0.085,0.14, "spin velocity  v = ½·log(t/2π)", "std(S) / v", [0.09,0.10,0.11,0.12,0.13,0.14])
pts=" ".join(f"{X(v):.1f},{Y(r):.1f}" for v,r in bands)
s.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="2"/>')
for v,r in bands:
    s.append(f'<circle cx="{X(v):.1f}" cy="{Y(r):.1f}" r="4.5" fill="{ACC}"/>')
    s.append(f'<text x="{X(v):.1f}" y="{Y(r)-9:.1f}" font-size="10.5" fill="{MUT}" text-anchor="middle">{r:.3f}</text>')
s.append('</svg>')
open("chart_speed.svg","w").write("\n".join(s))

# ---------- Chart 4: Rigidity — squeeze breaks it (Window 24) ----------
sq=[(0,0.15),(5,5.54),(20,5.18),(50,5.27),(90,13.80)]
s=frame("No Margin — squeezing the zeros", "Force the zeros tighter than their natural repulsion; reconstruction error explodes at 5%")
X,Y=axes(s, -3,95, 0,15, "squeeze  (%)", "reconstruction error", [0,3,6,9,12,15])
# bars
bw=10
for q,e in sq:
    xx=X(q)
    yy=Y(e)
    col=ACC if q>0 else ACC2
    s.append(f'<rect x="{xx-bw:.1f}" y="{yy:.1f}" width="{2*bw}" height="{(MT+PH)-yy:.1f}" fill="{col}" fill-opacity="0.82"/>')
    s.append(f'<text x="{xx:.1f}" y="{yy-6:.1f}" font-size="10.5" fill="{INK}" text-anchor="middle">{e:.2f}</text>')
    s.append(f'<text x="{xx:.1f}" y="{MT+PH+16:.1f}" font-size="10.5" fill="{MUT}" text-anchor="middle">{q}%</text>')
s.append('</svg>')
open("chart_rigidity.svg","w").write("\n".join(s))

print(">>> 4 SVG charts written: wind, swing, speed, rigidity")
