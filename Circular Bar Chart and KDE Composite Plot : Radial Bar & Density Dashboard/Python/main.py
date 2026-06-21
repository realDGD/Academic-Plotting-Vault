"""
图表：环形柱状图-核密度组合图 / 极坐标柱体与分布联动图 (Circular Bar Chart and KDE Composite Plot)
依赖：matplotlib, pandas, numpy, scipy
数据输入：Python/data_bar.csv, Python/data_kde.csv (用于分别提供柱状图与核密度图的数据)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon

def main():
    # Load data
    df_bar = pd.read_csv('Python/data_bar.csv')
    df_kde = pd.read_csv('Python/data_kde.csv')

    Name = df_bar['Name'].values
    Value = df_bar['Value'].values
    Len = df_bar['Len'].values
    Class = df_bar['Class'].values

    Num = df_kde['Num'].values
    NumClass = df_kde['NumClass'].values

    CList = np.array([
        [0.3961, 0.6863, 0.9529],
        [0.3686, 0.6039, 0.6118],
        [0.9725, 0.8039, 0.3137],
        [0.5020, 0.4706, 0.2902]
    ])
    ClassName = ['Class-A', 'Class-B', 'Class-C', 'Class-D']

    # Initialize figure
    fig = plt.figure(figsize=(11, 9))

    # ==============================
    # 1. Circular Bar Chart (ax1)
    # ==============================
    ax1 = fig.add_axes([0.05, 0.1, 0.9, 0.8])
    ax1.set_xlim(-1.75, 1)
    ax1.set_ylim(-1, 1)
    ax1.set_aspect('equal')
    ax1.axis('off')

    N = len(Value)
    M = np.max(Len)

    # Draw grid
    tt = np.linspace(np.pi/2, -np.pi/2, 100)
    xx = np.cos(tt)
    yy = np.sin(tt)

    for i in range(1, N + 1):
        r_factor = (i + 0.5) / (N + 0.5)
        ax1.plot(xx * r_factor, yy * r_factor, linewidth=1, color=np.array([1, 1, 1]) * 0.9, zorder=0)

    th = np.array([np.pi/2, -np.pi/2, np.pi/6, -np.pi/6])
    for t in th:
        ax1.plot([0, np.cos(t)], [0, np.sin(t)], linewidth=1, color=np.array([1, 1, 1]) * 0.9, zorder=0)

    # Draw bars
    for i in range(N):
        R = (N - i) / (N + 0.5)
        r = 0.3 / (N + 0.5)
        
        TT = (tt - np.pi/2) * 0.8 * Len[i] / M + np.pi/2
        
        X1 = np.cos(TT) * (R + r)
        X2 = np.cos(TT[::-1]) * (R - r)
        Y1 = np.sin(TT) * (R + r)
        Y2 = np.sin(TT[::-1]) * (R - r)
        
        X = np.concatenate([X1, X2])
        Y = np.concatenate([Y1, Y2])
        
        color = CList[Class[i] - 1]
        
        # In MATLAB, fill default edgecolor is black
        poly = Polygon(np.column_stack([X, Y]), facecolor=color, edgecolor='black', linewidth=1.5)
        ax1.add_patch(poly)
        
        tx = np.cos(TT[-1]) * R + np.sin(TT[-1]) / N / 2
        ty = np.sin(TT[-1]) * R - np.cos(TT[-1]) / N / 2
        ax1.text(tx, ty, str(Value[i]), ha='center', va='center', fontname='Arial', fontsize=13)
        
        ax1.text(-0.05, R, Name[i], ha='right', va='center', fontname='Arial', fontsize=13)

    # ax1 Legend
    legend_handles1 = []
    for i in range(np.max(Class)):
        color = CList[i]
        # Using a Polygon to match MATLAB's 'fill' patch behavior in legend
        patch = mpatches.Patch(facecolor=color, edgecolor='black', linewidth=1.5)
        legend_handles1.append(patch)

    fig.legend(legend_handles1, ClassName, frameon=False, prop={'family': 'Arial', 'size': 16, 'weight': 'bold'}, loc='upper left', bbox_to_anchor=(0.01, 0.88), borderaxespad=0, borderpad=0)

    # ==============================
    # 2. KDE Plot (ax2)
    # ==============================
    ax2 = fig.add_axes([0.05, 0.1, 0.536, 0.4])
    ax2.set_xlim(-20, 100)
    
    # Configure axes box and ticks
    ax2.tick_params(direction='out', length=3, width=1.5, labelsize=13)
    for spine in ax2.spines.values():
        spine.set_linewidth(1.5)
        spine.set_visible(True)
        
    ax2.set_xlabel('XXXX-XXXX-xxxxxxxx', fontname='Arial', fontsize=16)
    ax2.set_ylabel('Density', fontname='Arial', fontsize=16)
    ax2.axvline(40, color='black', linewidth=1, linestyle='--')

    legend_handles2 = []
    lgdtxt = []

    for i in range(1, np.max(NumClass) + 1):
        x = Num[NumClass == i]
        if len(x) == 0:
            continue
            
        kde = gaussian_kde(x)
        # Match ksdensity default limits: evaluate over the range
        xi = np.linspace(-20, 100, 200)
        f = kde(xi)
        
        color = CList[i - 1]
        ax2.fill_between(xi, 0, f, facecolor=color, alpha=0.5, edgecolor=color, linewidth=1.5)
        
        patch = mpatches.Patch(facecolor=color, alpha=0.5, edgecolor=color, linewidth=1.5)
        legend_handles2.append(patch)
        lgdtxt.append(f"Mean counts: {int(np.round(np.mean(x)))}")

    ax2.legend(legend_handles2, lgdtxt, frameon=False, prop={'family': 'Arial', 'size': 16}, loc='upper right')

    # Save figure
    plt.savefig('Python/result.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    main()
