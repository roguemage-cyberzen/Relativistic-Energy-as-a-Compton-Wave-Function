import mpmath as mp
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons
import numpy as np

# --- 1. Constants ---
mp.dps = 30 
c = mp.mpf('299792458')
hbar = mp.mpf('1.0545718e-34')
m_e = mp.mpf('9.10938356e-31') 
sigma_base = mp.mpf('1e-12') 

# --- 2. Plotting Setup ---
fig, ax = plt.subplots(figsize=(12, 8))
# Increase the bottom margin significantly to fit three rows of controls
plt.subplots_adjust(bottom=0.4, left=0.15)

x_width = 10e-12 
x_np = np.linspace(-x_width, x_width, 2000)
line_real, = ax.plot(x_np, np.zeros_like(x_np), label='Real Part (Re[Ψ])', color='blue', alpha=0.7)
line_env, = ax.plot(x_np, np.zeros_like(x_np), label='Envelope (|Ψ|)', color='black', linestyle='--')

ax.set_ylim(-1.2, 1.2)
ax.set_title("Relativistic Wave Packet: Follow Mode Centered")
ax.legend(loc='upper right')

# --- 3. UI Elements: Vertical Stack ---
# [left, bottom, width, height]
ax_v = plt.axes([0.25, 0.25, 0.5, 0.03])  # Top Slider
ax_t = plt.axes([0.25, 0.18, 0.5, 0.03])  # Middle Slider
ax_check = plt.axes([0.42, 0.05, 0.15, 0.08], frameon=False) # Bottom Checkbox

s_v = Slider(ax_v, 'Velocity (v/c)', 0.0, 0.999, valinit=0.1)
s_t = Slider(ax_t, 'Time (as)', 0.0, 5000.0, valinit=0.0, valstep=1.0)
check = CheckButtons(ax_check, ['Follow Mode'], [True])

# --- 4. Update Logic ---
def update(val):
    v_ratio = mp.mpf(s_v.val)
    t = mp.mpf(s_t.val) * mp.mpf('1e-18') 
    
    v = v_ratio * c
    gamma = 1 / mp.sqrt(1 - v_ratio**2)
    sigma = sigma_base / gamma
    
    omega = (gamma * m_e * c**2) / hbar
    k = (gamma * m_e * v) / hbar
    
    x_center = v * t
    
    is_following = check.get_status()[0]
    if is_following:
        view_min, view_max = float(x_center - x_width), float(x_center + x_width)
    else:
        view_min, view_max = -x_width, 5 * x_width

    current_x_mp = [mp.mpf(val) for val in np.linspace(view_min, view_max, 2000)]
    
    psi_real = [float(mp.exp(-(x - x_center)**2 / (2 * sigma**2)) * mp.cos(k*x - omega*t)) for x in current_x_mp]
    envelope = [float(mp.exp(-(x - x_center)**2 / (2 * sigma**2))) for x in current_x_mp]

    line_real.set_xdata(np.linspace(view_min, view_max, 2000))
    line_real.set_ydata(psi_real)
    line_env.set_xdata(np.linspace(view_min, view_max, 2000))
    line_env.set_ydata(envelope)
    
    ax.set_xlim(view_min, view_max)
    ax.set_title(f"v = {float(v_ratio):.3f}c | γ = {float(gamma):.2f} | Packet Pos: {float(x_center*1e12):.2f} pm")
    fig.canvas.draw_idle()

s_v.on_changed(update)
s_t.on_changed(update)
check.on_clicked(update)

update(0)
plt.show()