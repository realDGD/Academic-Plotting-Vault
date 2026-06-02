"""
图表：Segmented Circular Heatmap : Grouped Annular Heatmap
依赖：matplotlib, numpy, scipy
数据输入：data.json
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from matplotlib.colors import ListedColormap, Normalize
import re
import os

# Ensure the working directory is the Python directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. Load Data
with open('data.json', 'r') as f:
    data_dict = json.load(f)

Data = [np.array(d) for d in data_dict['Data']]
className = data_dict['className']
varNameRow = data_dict['varNameRow']
varNameCol = data_dict['varNameCol']
titleName = data_dict['titleName']

# 2. Parameters
sepRatio = 0.15
CMap = np.array([
    [9,100,203], [33,118,199], [61,137,200], [93,156,200],
    [123,174,201], [156,193,199], [182,209,199], [217,230,200],
    [251,249,200], [249,226,184], [251,203,167], [250,176,149],
    [249,151,130], [251,126,114], [252,100,95], [250,76,78],
    [249,52,61]
]) / 255.0

CLim = [-1, 1]
theta1 = np.pi
theta2 = -np.pi
R1 = 4.5
R2 = 8.0
R3 = 9.0
R4 = 10.0
thresholdValue = [-0.35, 0.35]

ringRatio = np.array([d.shape[1] for d in Data])
txtRatio = sepRatio / len(Data)
ringRatio1 = 1.0 / np.sum(ringRatio) * (1 - sepRatio)
ringRatio2 = ringRatio / np.sum(ringRatio) * (1 - sepRatio)

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.axis('off')
ax.set_xlim(-11, 11)
ax.set_ylim(-11, 11)

# Color interpolation
x = np.linspace(CLim[0], CLim[1], len(CMap))
pchip_r = PchipInterpolator(x, CMap[:, 0])
pchip_g = PchipInterpolator(x, CMap[:, 1])
pchip_b = PchipInterpolator(x, CMap[:, 2])

def get_color(val):
    val = np.clip(val, CLim[0], CLim[1])
    return (float(pchip_r(val)), float(pchip_g(val)), float(pchip_b(val)))

tS = np.linspace(0, 1, 50)

for k in range(len(Data)):
    theta3 = theta1 + (theta2 - theta1) * ((k + 1) * txtRatio + np.sum(ringRatio2[:k]))
    tData = Data[k]
    for i in range(tData.shape[0]):
        for j in range(tData.shape[1]):
            tT = theta3 + np.array([j, j + 1]) * ringRatio1 * (theta2 - theta1)
            tTd = tT[1] - tT[0]
            tT = np.array([tT[0] + tTd/30, tT[1] - tTd/30])
            
            tR = R2 + (R1 - R2) * np.array([i, i + 1]) / tData.shape[0]
            tRd = tR[1] - tR[0]
            tR = np.array([tR[0] + tRd/30, tR[1] - tRd/30])
            
            tT_poly = np.concatenate([
                tT[0] + (tT[1] - tT[0]) * tS,
                tT[1] + (tT[0] - tT[1]) * tS
            ])
            tR_poly = np.concatenate([
                tR[0] * np.ones(50),
                tR[1] * np.ones(50)
            ])
            
            val = tData[i, j]
            c = get_color(val)
            
            if val > thresholdValue[1] or val < thresholdValue[0]:
                ax.fill(tR_poly * np.cos(tT_poly), tR_poly * np.sin(tT_poly), color=c, edgecolor='black', linewidth=1.2, alpha=0.8)
            else:
                ax.fill(tR_poly * np.cos(tT_poly), tR_poly * np.sin(tT_poly), color=c, edgecolor='white', linewidth=1.2)
                
    for i in range(tData.shape[0]):
        for j in range(tData.shape[1]):
            tT = theta3 + np.array([j, j + 1]) * ringRatio1 * (theta2 - theta1)
            tR = R2 + (R1 - R2) * np.array([i, i + 1]) / tData.shape[0]
            tR_mean = np.mean(tR)
            tT_mean = np.mean(tT)
            
            rot_tT = (tT_mean + np.pi) % (2*np.pi) - np.pi
            if rot_tT < 0 and rot_tT > -np.pi:
                rot = rot_tT / np.pi * 180 + 90
            else:
                rot = rot_tT / np.pi * 180 - 90
                
            ax.text(tR_mean * np.cos(tT_mean), tR_mean * np.sin(tT_mean), str(tData[i, j]), 
                    rotation=rot, color='black', ha='center', va='center', fontsize=9)

ax.text(0, 0, titleName, ha='center', va='center', fontsize=18)

# Add Text 1 (Rows)
for k in range(len(Data)):
    tT = theta1 + (theta2 - theta1) * ((k + 0.5) * txtRatio + np.sum(ringRatio2[:k]))
    for i in range(Data[k].shape[0]):
        tR = R2 + (R1 - R2) * np.array([i, i + 1]) / Data[k].shape[0]
        tR_mean = np.mean(tR)
        
        rot_tT = (tT + np.pi) % (2*np.pi) - np.pi
        if rot_tT < 0 and rot_tT > -np.pi:
            rot = rot_tT / np.pi * 180 + 90
        else:
            rot = rot_tT / np.pi * 180 - 90
            
        ax.text(tR_mean * np.cos(tT), tR_mean * np.sin(tT), varNameRow[k][i],
                rotation=rot, color='black', ha='center', va='center', fontsize=12)

# Add Text 2 (Columns)
for k in range(len(Data)):
    theta3 = theta1 + (theta2 - theta1) * ((k + 1) * txtRatio + np.sum(ringRatio2[:k]))
    tR = (R2 * 3 + R3 * 2) / 5.0
    for j in range(Data[k].shape[1]):
        tT = theta3 + np.array([j, j + 1]) * ringRatio1 * (theta2 - theta1)
        tT_mean = np.mean(tT)
        
        rot_tT = (tT_mean + np.pi) % (2*np.pi) - np.pi
        if rot_tT < 0 and rot_tT > -np.pi:
            rot = rot_tT / np.pi * 180 + 90
        else:
            rot = rot_tT / np.pi * 180 - 90
            
        s = varNameCol[k][j].replace('_{', '$_{').replace('}', '}$')
        ax.text(tR * np.cos(tT_mean), tR * np.sin(tT_mean), s,
                rotation=rot, color='black', ha='center', va='center', fontsize=12)

# Add Text 3 (Class Name)
tS_100 = np.linspace(0, 1, 100)
for k in range(len(Data)):
    theta3 = theta1 + (theta2 - theta1) * (k * txtRatio + np.sum(ringRatio2[:k]))
    theta4 = theta1 + (theta2 - theta1) * ((k + 1) * txtRatio + np.sum(ringRatio2[:k+1]))
    
    tT = np.array([theta3, theta4])
    tT[0] = tT[0] - 2 * np.pi / 40 / len(Data)
    
    tR = np.array([R3, R4])
    ttT_mean = np.mean(tT)
    ttR_mean = np.mean(tR)
    
    tT_poly = np.concatenate([
        tT[0] + (tT[1] - tT[0]) * tS_100,
        tT[1] + (tT[0] - tT[1]) * tS_100
    ])
    tR_poly = np.concatenate([
        tR[0] * np.ones(100),
        tR[1] * np.ones(100)
    ])
    
    # In MATLAB: fill(..., 'EdgeColor', [.3,.3,.3], 'LineWidth', 1.2, 'EdgeAlpha', .8)
    # matplotlib fill cannot do EdgeAlpha separately unless using PathPatch or setting alpha to the whole patch.
    # We will just draw a fill without edge, and plot the edge separately to avoid alpha on facecolor.
    ax.fill(tR_poly * np.cos(tT_poly), tR_poly * np.sin(tT_poly), color='white')
    
    tT_poly_closed = np.append(tT_poly, tT_poly[0])
    tR_poly_closed = np.append(tR_poly, tR_poly[0])
    ax.plot(tR_poly_closed * np.cos(tT_poly_closed), tR_poly_closed * np.sin(tT_poly_closed), color=[0.3, 0.3, 0.3, 0.8], linewidth=1.2)
    
    rot_tT = (ttT_mean + np.pi) % (2*np.pi) - np.pi
    if rot_tT < 0 and rot_tT > -np.pi:
        rot = rot_tT / np.pi * 180 + 90
    else:
        rot = rot_tT / np.pi * 180 - 90
        
    ax.text(ttR_mean * np.cos(ttT_mean), ttR_mean * np.sin(ttT_mean), className[k],
            rotation=rot, color='black', ha='center', va='center', fontsize=12)

# Colorbar
vals = np.linspace(-1, 1, 256)
colors = [get_color(v) for v in vals]
cmap = ListedColormap(colors)
norm = Normalize(vmin=-1, vmax=1)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Adjust cb position to bottom, similar to matlab
# Location="southoutside"
cax = fig.add_axes([0.3, 0.05, 0.4, 0.02]) # [left, bottom, width, height]
cbar = fig.colorbar(sm, cax=cax, orientation='horizontal')
cax.text(-0.03, 0.5, 'Correlation\ncoefficient r', transform=cax.transAxes, ha='right', va='center', fontsize=12)
cbar.ax.tick_params(labelsize=10, direction='out', length=3)
cbar.ax.set_xticks([-1, -0.5, 0, 0.5, 1])

plt.savefig('result.png', dpi=300, bbox_inches='tight')
