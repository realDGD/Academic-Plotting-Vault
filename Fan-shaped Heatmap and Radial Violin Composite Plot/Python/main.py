"""
图表：Fan-shaped Heatmap and Radial Violin Composite Plot
依赖：matplotlib, numpy, pandas, scipy
数据输入：data.csv
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from scipy.stats import gaussian_kde
import os

# Ensure working directory is correct
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Load data
data_df = pd.read_csv('data.csv')
Data = data_df.iloc[:7].values
VData = data_df.iloc[7:].values

rowName = [str(y) for y in range(2024, 2017, -1)]
colName = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Plot parameters
font_prop = {'fontsize': 16, 'fontname': 'Times New Roman'}
cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', ['#D17A93', '#FFFFFF', '#6E95B7'])
width = 0.9

# Data scaling
vmin = np.min(Data)
vmax = np.max(Data)
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

VLim = [min(np.min(Data), np.min(VData)), max(np.max(Data), np.max(VData))]
linearTickCompactDegree = 5
tXS = (VLim[1] - VLim[0]) / linearTickCompactDegree
tXN = np.ceil(np.log10(tXS))
tXS = np.round(np.round(tXS / 10**(tXN-2)) / 5) * 5 * 10**(tXN-2)
tVTick1 = np.arange(0, VLim[0] - tXS*1.1, -tXS)
tVTick2 = np.arange(0, VLim[1] + tXS*1.1, tXS)
VTick = np.unique(np.concatenate([tVTick1, tVTick2]))
VTick = VTick[(VTick >= VLim[0]) & (VTick <= VLim[1])]

# Calculate violins
maxf = 0
kdes = []
y_evals = []
for i in range(12):
    tY = VData[:, i]
    tY = tY[~np.isnan(tY)]
    kde = gaussian_kde(tY)
    kdes.append(kde)
    yi = np.linspace(tY.min(), tY.max(), 100)
    y_evals.append(yi)
    maxf = max(maxf, np.max(kde(yi)))

fig = plt.figure(figsize=(12, 10), facecolor='w')
ax = fig.add_axes([0.05, 0.2, 0.9, 0.8])
ax.set_xlim(-np.sqrt(3), np.sqrt(3))
ax.set_ylim(0, 2)
ax.set_aspect('equal')
ax.axis('off')

# Rays
w = np.pi / 3 / Data.shape[1]
tt_col = np.linspace(5*np.pi/6 - w, np.pi/6 + w, Data.shape[1])
for i in range(Data.shape[1]):
    ax.plot([0, np.cos(tt_col[i])*2], [0, np.sin(tt_col[i])*2], '--', color=[0.8, 0.8, 0.8], linewidth=1)

# Col labels
for i in range(len(colName)):
    ax.text(np.cos(tt_col[i])*2.01, np.sin(tt_col[i])*2.01, colName[i],
            ha='center', va='bottom', rotation_mode='anchor', rotation=np.degrees(tt_col[i]) - 90, **font_prop)

# Row labels
for i in range(len(rowName)):
    r = 2/5 + (Data.shape[0] - (i+1) + 0.5) * 4 / Data.shape[0] / 5
    if (i+1) % 2 == 1:
        ax.text(np.cos(5*np.pi/6)*r - 0.01, np.sin(5*np.pi/6)*r - np.sqrt(3)/100, rowName[i],
                ha='right', va='center_baseline', rotation_mode='anchor', rotation=60, **font_prop)
    else:
        ax.text(np.cos(np.pi/6)*r + 0.01, np.sin(np.pi/6)*r - np.sqrt(3)/100, rowName[i],
                ha='left', va='center_baseline', rotation_mode='anchor', rotation=-60, **font_prop)

# Tick axis
ax.plot(np.cos(5*np.pi/6)*np.array([1.3, 1.9]), np.sin(5*np.pi/6)*np.array([1.3, 1.9]), 'k-', linewidth=1)
ax.plot(np.cos(np.pi/6)*np.array([1.3, 1.9]), np.sin(np.pi/6)*np.array([1.3, 1.9]), 'k-', linewidth=1)

# Ticks
for i, vt in enumerate(VTick):
    r = (vt - VLim[0]) / (VLim[1] - VLim[0]) * 0.6 + 1.3
    
    x1 = [np.cos(5*np.pi/6)*r, np.cos(5*np.pi/6)*r + 0.01]
    y1 = [np.sin(5*np.pi/6)*r, np.sin(5*np.pi/6)*r + np.sqrt(3)/100]
    ax.plot(x1, y1, 'k-', linewidth=1)
    
    x2 = [np.cos(np.pi/6)*r, np.cos(np.pi/6)*r - 0.01]
    y2 = [np.sin(np.pi/6)*r, np.sin(np.pi/6)*r + np.sqrt(3)/100]
    ax.plot(x2, y2, 'k-', linewidth=1)
    
    val_str = f"{vt:.2g}"
    if (len(VTick) - (i+1)) % 2 == 0:
        ax.text(np.cos(5*np.pi/6)*r - 0.01, np.sin(5*np.pi/6)*r - np.sqrt(3)/100, val_str,
                ha='right', va='center_baseline', rotation_mode='anchor', rotation=60, **font_prop)
    else:
        ax.text(np.cos(np.pi/6)*r + 0.01, np.sin(np.pi/6)*r - np.sqrt(3)/100, val_str,
                ha='left', va='center_baseline', rotation_mode='anchor', rotation=-60, **font_prop)

# Violins
for i in range(Data.shape[1]):
    tY = VData[:, i]
    tY = tY[~np.isnan(tY)]
    yi = y_evals[i]
    f = kdes[i](yi)
    
    xx = np.concatenate([f, -f[::-1]]) / maxf * (4*np.pi/5 / Data.shape[1]) * width / 2
    yy_mapped = (yi - VLim[0]) / (VLim[1] - VLim[0]) * 0.6 + 1.3
    yy = np.concatenate([yy_mapped, yy_mapped[::-1]])
    
    R = np.array([[np.cos(tt_col[i] - np.pi/2), -np.sin(tt_col[i] - np.pi/2)],
                  [np.sin(tt_col[i] - np.pi/2), np.cos(tt_col[i] - np.pi/2)]])
    xy = np.dot(R, np.vstack([xx, yy]))
    
    mean_val = np.mean(tY)
    color = cmap(norm(mean_val))
    ax.fill(xy[0, :], xy[1, :], facecolor=color, edgecolor='k', linewidth=1, zorder=3)
    
    # Quartiles
    qt25 = np.percentile(tY, 25)
    qt75 = np.percentile(tY, 75)
    med = np.median(tY)
    
    f3 = kdes[i](qt25)[0]
    f4 = kdes[i](qt75)[0]
    f5 = kdes[i](med)[0]
    
    xx_q = np.array([f3, -f3, f4, -f4, f5, -f5]) / maxf * (4*np.pi/5 / Data.shape[1]) * width / 2
    yy_q = (np.array([qt25, qt25, qt75, qt75, med, med]) - VLim[0]) / (VLim[1] - VLim[0]) * 0.6 + 1.3
    
    xy_q = np.dot(R, np.vstack([xx_q, yy_q]))
    
    ax.plot(xy_q[0, 0:2], xy_q[1, 0:2], 'k-', linewidth=1, zorder=4)
    ax.plot(xy_q[0, 2:4], xy_q[1, 2:4], 'k-', linewidth=1, zorder=4)
    ax.plot(xy_q[0, 4:6], xy_q[1, 4:6], 'k-', linewidth=2, zorder=4)

# Heatmap
TT = np.linspace(5*np.pi/6, np.pi/6, Data.shape[1] + 1)
for i in range(Data.shape[0]):
    for j in range(Data.shape[1]):
        tt = np.linspace(TT[j], TT[j+1], 30)
        r1 = 0.4 + i * 4 / Data.shape[0] / 5
        r2 = 0.4 + (i + 1) * 4 / Data.shape[0] / 5
        
        xx = np.concatenate([np.cos(tt)*r1, np.cos(tt[::-1])*r2])
        yy = np.concatenate([np.sin(tt)*r1, np.sin(tt[::-1])*r2])
        
        color = cmap(norm(Data[i, j]))
        ax.fill(xx, yy, facecolor=color, edgecolor='w', linewidth=1, zorder=2)

# Top arc
tt_arc = np.linspace(5*np.pi/6, np.pi/6, 80)
ax.plot(np.cos(tt_arc)*2, np.sin(tt_arc)*2, 'k-', linewidth=1, zorder=2)

# Colorbar
cbar_ax = fig.add_axes([0.49, 0.1, 0.02, 0.2])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax)
cbar.ax.yaxis.set_ticks_position('left')
cbar.ax.tick_params(labelsize=16, direction='in')

ticks = cbar.get_ticks()
# Filter ticks to only those within vmin and vmax to be safe
ticks = ticks[(ticks >= vmin) & (ticks <= vmax)]
cbar.set_ticks(ticks)
cbar.ax.set_ylim(vmin, vmax) # Prevent axes expansion causing white areas

labels = [f"{t:.2g}" for t in ticks]
if len(labels) > 1:
    labels[-1] = ""  # Hide only the top tick
cbar.ax.set_yticklabels(labels)

for l in cbar.ax.yaxis.get_ticklabels():
    l.set_fontname('Times New Roman')

plt.savefig('result.png', dpi=300, bbox_inches='tight')
