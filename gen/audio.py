# 10秒動画の音（BGM＋効果音）を作る。すべてプログラムで合成するので著作権の心配なし。
# 使い方: python3 -I audio.py quiz|promo seed out.wav
import sys, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 48000
import os
DUR = float(os.environ.get('DUR_S', '10'))
N = int(SR * DUR)

def t_(d): return np.arange(int(SR * d)) / SR
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)

def add(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    x = x[:len(buf) - i]
    buf[i:i + len(x)] += g * x

def piano(m, d=2.2, vel=1.0):
    f = midi(m); t = t_(d); y = np.zeros_like(t)
    for k, a in enumerate([1, .55, .32, .18, .1, .06], 1):
        fk = f * k * (1 + 0.0004 * k * k)
        y += a * np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.2 + 0.9 * k))
    att = np.minimum(1, t / 0.004)
    hammer = np.random.randn(len(t)) * np.exp(-t * 90) * 0.04
    return (y * att + hp(hammer, 1500)) * vel * 0.22

def pad(ms, d):
    t = t_(d); y = np.zeros_like(t)
    for m in ms:
        for det in (-0.07, 0.0, 0.08):
            f = midi(m) * 2 ** (det / 12)
            ph = np.random.rand()
            y += 2 * ((f * t + ph) % 1) - 1
    y = lp(y, 1400, 2) / (len(ms) * 3)
    env = np.minimum(1, t / 0.8) * np.minimum(1, (d - t) / 0.6)
    return y * env * 0.09

def bass(m, d):
    t = t_(d); f = midi(m)
    y = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    return y * np.minimum(1, t / 0.05) * np.exp(-t * 0.6) * np.minimum(1, (d - t) / 0.2) * 0.13

def reverb(x, dec=2.4, mix=0.32):
    t = t_(dec); out = []
    for s in (1, 2):
        ir = np.random.RandomState(s).randn(len(t)) * np.exp(-t * 6.9 / dec)
        ir = lp(ir, 5000); ir /= np.sqrt((ir ** 2).sum())
        out.append(fftconvolve(x, ir)[:len(x)])
    return np.stack([x * (1 - mix) + o * mix * 1.4 for o in out], 1)

def music(kind, seed):
    rng = np.random.RandomState(seed); np.random.seed(seed)
    buf = np.zeros(N)
    if kind in ('quiz','rank'):   # D: Dmaj9 Bm7 Gmaj7 Asus-A
        prog = [(50, [62, 66, 69, 73, 76]), (47, [59, 62, 66, 69, 74]), (43, [59, 62, 66, 71, 74]), (45, [57, 62, 64, 69, 73])]
    else:                # G: Gmaj9 Em9 Cmaj7 D (promo / ad)
        prog = [(43, [55, 59, 62, 66, 69]), (40, [55, 59, 62, 66, 71]), (48, [55, 59, 64, 67, 71]), (50, [57, 62, 66, 69, 74])]
    seg = DUR / 4; step = seg / 8
    pat = [0, 2, 4, 3, 1, 3, 4, 2]
    for i, (root, notes) in enumerate(prog):
        t0 = i * seg
        add(buf, pad(notes[:4], seg + 0.6), t0)
        add(buf, bass(root, seg + 0.1), t0)
        for j, p in enumerate(pat):
            vel = 0.75 + 0.25 * rng.rand() if j else 1.0
            add(buf, piano(notes[p] + 12, 2.0, vel), t0 + j * step + rng.rand() * 0.006)
    return buf

def whoosh(d=0.45):
    t = t_(d); n = np.random.randn(len(t))
    y = np.zeros_like(t)
    for k in range(8):
        s = slice(k * len(t) // 8, (k + 1) * len(t) // 8)
        lo = 300 + 3000 * k / 8
        y[s] = bp(n, lo, lo * 2.2)[s]
    return y * np.sin(np.pi * t / d) ** 2 * 0.22

def tick(hi=False):
    t = t_(0.11); f = 1500 if hi else 1150
    body = np.sin(2 * np.pi * f * t) * np.exp(-t * 38) + 0.5 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 60)
    click = hp(np.random.randn(len(t)), 2500) * np.exp(-t * 300) * 0.8
    return (body + click) * 0.32

def beep(f=1320, d=0.16):
    t = t_(d); return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.004) * np.exp(-t * 14) * 0.13

def bell(f=1568, d=2.4, g=0.2):
    t = t_(d); mod = np.sin(2 * np.pi * f * 3.5 * t) * 2.2 * np.exp(-t * 3)
    return np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 2.2) * g

def sparkle(d=1.2, n=70, seed=3):
    r = np.random.RandomState(seed); buf = np.zeros(int(SR * d))
    for _ in range(n):
        at = r.rand() ** 1.6 * (d - 0.15); f = 3000 + r.rand() * 5000; tt = t_(0.12)
        add(buf, np.sin(2 * np.pi * f * tt) * np.exp(-tt * 45) * (0.03 + 0.04 * r.rand()) * (1 - at / d), at)
    return buf

def build(kind, seed):
    np.random.seed(seed)
    m = music(kind, seed)
    fx = np.zeros(N); dry = np.zeros(N); duck = np.ones(N)
    if kind == 'quiz':
        TQ, TA, TE = 2.1, 5.6, 7.7
        add(fx, whoosh(), TQ - 0.2)
        t = TQ + 0.5; k = 0
        # 焦らせる：チクタクを速く、最後の1秒はさらに倍速
        while t < TA - 0.02:
            add(dry, tick(k % 2 == 0), t); k += 1
            t += 0.25 if t < TA - 1.0 else 0.125
        for c in range(3): add(dry, beep(1175 + 220 * c, 0.3) * 2.2, TQ + 0.5 + c * 1.0)
        # 心臓の鼓動（ドクン、ドクン）。だんだん速く・強く
        hb = TQ + 0.5; gap = 0.5
        while hb < TA - 0.05:
            for off, g in ((0, 1.0), (0.16, 0.65)):
                tt = t_(0.22); f0 = 58
                add(fx, np.sin(2*np.pi*f0*tt*(1-0.25*tt)) * np.exp(-tt*16) * 0.55 * g * (0.7 + 0.3*(hb-TQ)/3.5), hb + off)
            gap = max(0.3, gap - 0.04); hb += gap
        # だんだん高く大きくなる音
        rd = TA - (TQ + 0.5); rt = t_(rd)
        freq = 380 * (2.4 ** (rt / rd)); ph = 2*np.pi*np.cumsum(freq)/SR
        riser = (np.sin(ph) + 0.4*np.sin(2*ph)) * (rt/rd)**2 * 0.07
        add(fx, riser * np.minimum(1, (rd - rt)/0.03), TQ + 0.5)
        add(fx, bell(1568), TA); add(fx, bell(2349, 2.0, 0.09), TA + 0.02); add(fx, sparkle(), TA + 0.03)
        add(fx, whoosh(0.5), TE - 0.25); add(fx, bell(1175, 2.2, 0.08), TE + 0.1)
        a, b = int((TQ + 0.4) * SR), int(TA * SR)
        duck[a:b] = 0.07
    elif kind == 'rank':
        for t in (1.2, 3.0, 4.8, 6.6): add(fx, whoosh(0.4), t - 0.15); add(fx, beep(990, 0.15) * 1.2, t + 0.05)
        # ドラムロール（だんだん速く・大きく）
        t = 8.6; gap = 0.07
        while t < 9.45:
            tt = t_(0.05); sn = bp(np.random.randn(len(tt)), 900, 6000) * np.exp(-tt * 60)
            add(dry, sn * (0.25 + 0.5 * (t - 8.6) / 0.85), t); t += gap; gap = max(0.035, gap * 0.95)
        tt = t_(0.5); add(dry, np.sin(2*np.pi*55*tt*(1-0.3*tt)) * np.exp(-tt*7) * 0.9, 9.5)
        add(fx, bell(1568, 2.6, 0.18), 9.5); add(fx, bell(2349, 2.2, 0.08), 9.52); add(fx, sparkle(1.2, 80, 7), 9.53)
        add(fx, whoosh(0.5), 11.75); add(fx, bell(1175, 2.2, 0.08), 12.1)
        a, b = int(8.5 * SR), int(9.5 * SR); duck[a:b] = 0.25
    elif kind == 'ad':
        for t in (3.6, 6.6, 10.6, 14.6): add(fx, whoosh(0.5), t - 0.25)
        add(fx, bell(1318, 2.6, 0.12), 3.75); add(fx, bell(1568, 2.6, 0.12), 10.9); add(fx, sparkle(1.0, 40, 5), 11.0); add(fx, bell(1760, 2.2, 0.08), 14.75)
    else:
        TS, TE = 3.0, 6.8
        add(fx, whoosh(0.55), TS - 0.25); add(fx, bell(1318, 2.6, 0.13), TS + 0.15); add(fx, sparkle(1.0, 40, 5), TS + 0.18)
        add(fx, whoosh(0.5), TE - 0.25); add(fx, bell(1760, 2.2, 0.08), TE + 0.15)
    duck = lp(duck, 6)
    mix = m * duck + fx * 0.9
    st = reverb(mix) + 1.7 * dry[:, None]
    fade = np.ones(N); fade[:int(.02 * SR)] = np.linspace(0, 1, int(.02 * SR)); fade[-int(.5 * SR):] = np.linspace(1, 0, int(.5 * SR))
    st *= fade[:, None]
    st /= np.abs(st).max() / 0.89
    return st

if __name__ == '__main__':
    kind, seed, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    wavfile.write(out, SR, (build(kind, seed) * 32767).astype(np.int16))
