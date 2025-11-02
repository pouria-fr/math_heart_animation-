import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

STYLE = "classic" 

def stylize(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect('equal', adjustable='box')
    if STYLE == "classic":
        ax.axis('on')
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.figure.patch.set_facecolor('white')
        ax.set_facecolor('white')
        color = 'C0'
    else:
        ax.axis('off')
        ax.figure.patch.set_facecolor('black')
        ax.set_facecolor('black')
        for s in ax.spines.values(): s.set_color('white')
        ax.tick_params(colors='white')
        color = 'C0'
    return color

xmax = np.sqrt(3.0)
x = np.linspace(-xmax, xmax, 4000)
base = np.abs(x) ** (2/3)
envelope = np.sqrt(np.clip(3 - x**2, 0, None))

fig1, ax1 = plt.subplots(figsize=(6,6))
line_color = stylize(ax1, (-2.0, 2.0), (-1.5, 3.0))
(line1,) = ax1.plot([], [], lw=2.2, color=line_color)

FPS = 40
BEATS_PER_SEC = 0.6
WAVE_CYCLES_PER_SEC = 0.8
A_BASE = 0.70
A_VAR  = 0.06
frames = int(10*FPS)

def cartesian_frame(i):
    t = i / FPS
    a   = A_BASE + A_VAR * np.sin(2*np.pi*BEATS_PER_SEC*t)
    phi = 2*np.pi*WAVE_CYCLES_PER_SEC*t
    y = base + a * np.sin(89*x + phi) * envelope
    line1.set_data(x, y)
    return (line1,)

anim1 = FuncAnimation(fig1, cartesian_frame, frames=frames, interval=1000/FPS, blit=True)

th = np.linspace(0, 2*np.pi, 4000)
num = np.sqrt(np.abs(np.cos(th)))
den = (np.sin(th) + 7.0/5.0)
r = np.sin(th)*(num/den) - 2*np.sin(th) + 2
xp, yp = r*np.cos(th), r*np.sin(th)

fig2, ax2 = plt.subplots(figsize=(6,6))
line_color2 = stylize(ax2, (-4, 4), (-4, 4))
(line2,) = ax2.plot([], [], lw=2.2, color=line_color2)

def polar_frame(i):
    n = min(20 + i*12, len(xp))
    line2.set_data(xp[:n], yp[:n])
    return (line2,)

anim2 = FuncAnimation(fig2, polar_frame, frames=350, interval=20, blit=True)

def save(anim, fname, fps=30):
    try:
        anim.save(fname, writer=FFMpegWriter(fps=fps))
        print("Saved:", fname)
    except Exception:
        anim.save(fname.replace(".mp4",".gif"), writer=PillowWriter(fps=fps//2))
        print("Saved:", fname.replace(".mp4",".gif"))

if __name__ == "__main__":
    save(anim1, "heart_cartesian.mp4", fps=40)
    save(anim2, "heart_polar.mp4", fps=40)
