"""
图表：高级定制雷达图 / 极简多维特征蜘蛛图 (Advanced Customized Radar Chart / Minimalist Multi-dimensional Spider Plot)
依赖：matplotlib, pandas, numpy
数据输入：Python/data.csv，其中第一列为Class，后续列为各维度特征
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from shapely.geometry import Polygon

def main():
    # Load data
    data_path = os.path.join(os.path.dirname(__file__), 'data.csv')
    df = pd.read_csv(data_path)
    
    classes = df['Class'].tolist()
    prop_names = df.columns[1:].tolist()
    data = df.iloc[:, 1:].values
    
    num_props = len(prop_names)
    
    # Chart configurations
    r_lim = [0, 1]
    r_tick = [0, 0.5, 1]
    r_range = [0.1, 1]
    rotation = np.pi / 2
    
    # Colors
    c_list = [
        (151/255, 125/255, 154/255),
        (179/255, 97/255, 97/255)
    ]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Draw background circular fill
    tt = np.linspace(0, 2 * np.pi, 200)
    ax.fill(np.cos(tt), np.sin(tt), color=(252/255, 252/255, 252/255), zorder=0)
    
    # Calculate angles
    theta = np.linspace(0, 2 * np.pi, num_props, endpoint=False)
    theta = theta + rotation
    # Reverse direction (clockwise)
    theta = np.concatenate(([theta[0]], theta[:0:-1]))
    
    # Draw Theta tick lines (spokes)
    for t in theta:
        x = [np.cos(t) * r_range[0], np.cos(t) * r_range[1]]
        y = [np.sin(t) * r_range[0], np.sin(t) * r_range[1]]
        ax.plot(x, y, color=(200/255, 200/255, 200/255), linewidth=2, zorder=2)
        
    # Draw R tick lines (dashed circles)
    for tick in r_tick:
        r = (tick - r_lim[0]) / (r_lim[1] - r_lim[0]) * (r_range[1] - r_range[0]) + r_range[0]
        ax.plot(r * np.cos(tt), r * np.sin(tt), color='#C9C9C9', linewidth=2, linestyle='--', zorder=3)
        
    # Draw radar chart fills using Shapely for exact colors
    polys = []
    xps, yps = [], []
    for row in data:
        r_data = (row - r_lim[0]) / (r_lim[1] - r_lim[0]) * (r_range[1] - r_range[0]) + r_range[0]
        xp = np.cos(theta) * r_data
        yp = np.sin(theta) * r_data
        xp = np.append(xp, xp[0])
        yp = np.append(yp, yp[0])
        xps.append(xp)
        yps.append(yp)
        polys.append(Polygon(zip(xp, yp)))

    stalk_poly = polys[0]
    tip_poly = polys[1]
    
    stalk_only = stalk_poly.difference(tip_poly)
    tip_only = tip_poly.difference(stalk_poly)
    overlap = stalk_poly.intersection(tip_poly)

    def plot_poly(geom, color):
        if geom.is_empty: return
        if geom.geom_type == 'Polygon':
            ax.fill(*geom.exterior.xy, color=color, zorder=1)
        elif geom.geom_type == 'MultiPolygon':
            for p in geom.geoms:
                ax.fill(*p.exterior.xy, color=color, zorder=1)

    plot_poly(stalk_only, '#E9E4E8')
    plot_poly(tip_only, '#EEDDDE')
    plot_poly(overlap, '#DECACE')

    # Draw radar chart lines on top
    lines = []
    for i in range(len(data)):
        line, = ax.plot(xps[i], yps[i], color=c_list[i], marker='o', linewidth=5, markersize=14, markerfacecolor=c_list[i], zorder=4)
        lines.append(line)
        
    # Draw property labels
    for i, prop in enumerate(prop_names):
        x = np.cos(theta[i]) * 1.15
        y = np.sin(theta[i]) * 1.15
        
        # Adjust alignment based on position
        ha = 'center'
        va = 'center'
        if x > 0.1: ha = 'left'
        elif x < -0.1: ha = 'right'
        if y > 0.1: va = 'bottom'
        elif y < -0.1: va = 'top'
            
        ax.text(x, y, prop, fontname='Times New Roman', fontsize=21, ha=ha, va=va)
        
    # Legend
    legend = ax.legend(lines, classes, loc='upper right', prop={'family': 'Times New Roman', 'size': 21})
    
    # Adjust limits to fit labels
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    
    # Save figure
    out_path = os.path.join(os.path.dirname(__file__), 'result.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    main()
