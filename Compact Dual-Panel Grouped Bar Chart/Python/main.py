import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Set figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 5.5))

# Data
YData = np.array([
    [0.7772,    1.0363,    0.7772,    1.0363,    2.7202],
    [3.4974,    5.3109,    4.2746,    4.0155,   12.9534],
    [3.4974,    3.7565,    3.1088,    3.8860,   14.8964],
    [1.9430,    2.3316,    2.3316,    2.7202,    2.7202],
    [17.2280,  19.9482,   17.0984,   19.0415,   22.6684],
    [0.2591,    0.3886,    0.3886,    0.3886,    2.5907]
])

YData1 = YData
YData2 = YData

# Colors (normalized to 0-1)
CData = np.array([
    [111, 173,  72],
    [ 92, 154, 215],
    [255, 192,   1],
    [ 69, 103,  42],
    [ 36,  94, 144]
]) / 255.0

labels = ['SO2', 'NO2', 'PM10', 'PM2.5', 'O3', 'CO']
legend_labels = ['FNN', 'RF', 'XGBoost', 'SVR', 'WRF-CMAQ']

# Bar settings
n_groups = YData.shape[0]
n_bars = YData.shape[1]
index = np.arange(1, n_groups + 1)
# Create gaps between bars, similar to Matlab's default
step = 0.15       # Distance between the centers of adjacent bars
bar_width = 0.12  # Width of each bar (leaving a gap)
offsets = np.arange(-n_bars/2 + 0.5, n_bars/2) * step

# Font properties
font_prop = {'family': 'Cambria', 'weight': 'bold', 'size': 12}
font_legend = {'family': 'Cambria', 'weight': 'bold', 'size': 13}
font_text = {'family': 'Cambria', 'weight': 'bold', 'size': 15}

# Plot
for i in range(n_bars):
    ax1.bar(index + offsets[i], YData1[:, i], bar_width, color=CData[i], edgecolor='none', label=legend_labels[i], zorder=3)
    ax2.bar(index + offsets[i], YData2[:, i], bar_width, color=CData[i], edgecolor='none', label=legend_labels[i], zorder=3)

# Function to decorate axes
def decorate_ax(ax):
    ax.set_xticks(index)
    ax.set_xticklabels(labels, fontdict=font_prop)
    for label in ax.get_yticklabels():
        label.set_fontproperties(FontProperties(**font_prop))
        
    # Grid (X axis only, dashed or solid? Matlab's grid is solid usually with alpha)
    ax.grid(axis='x', alpha=0.2, zorder=0)
    
    # Spines (Box)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color('black')
        
    # Ticks
    ax.tick_params(axis='both', length=0)
    
    # X and Y axis limits to ensure groups are centered and texts don't overlap
    ax.set_xlim(0.5, n_groups + 0.5)
    ax.set_ylim(0, 26)
    
    # Vertical lines between groups
    for x in np.arange(1.5, n_groups):
        ax.axvline(x=x, color='black', linestyle='--', linewidth=1.4, zorder=1)

decorate_ax(ax1)
decorate_ax(ax2)

# Legends
# In Matlab, both legends are southoutside, and the layout adjusts. 
# We'll place them below each subplot.
for ax in (ax1, ax2):
    # Adjust handlelength/handleheight to shrink the square (Matlab used 8x8 with font size 13, roughly 0.6 times font size)
    # Adjust handletextpad to reduce distance between square and text
    leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=n_bars, frameon=False, prop=FontProperties(**font_legend), handlelength=0.6, handleheight=0.6, handletextpad=0.2, columnspacing=0.6)

# Texts inside plot
# Matlab places them at x=0.6, y=22.5. 0.6 is left of the first bar group.
ax1.text(0.6, 22.5, 'MAE', fontdict=font_text)
ax2.text(0.6, 22.5, 'RMSE', fontdict=font_text)

# Adjust layout
plt.subplots_adjust(left=0.08, right=0.98, bottom=0.1, top=0.95, hspace=0.35)

# Save image
plt.savefig('result.png', dpi=300, bbox_inches='tight')
