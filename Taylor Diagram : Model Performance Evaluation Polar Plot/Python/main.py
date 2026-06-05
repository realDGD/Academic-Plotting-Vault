"""
图表：Taylor Diagram / Model Performance Evaluation Polar Plot
依赖：matplotlib, pandas, numpy
数据输入：Python/data.csv，其中第一列为参考观测数据(Reference)，后续各列为模型预测数据(Models)。
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec

def SStats(Cr, Cf):
    Cr = np.asarray(Cr).flatten()
    Cf = np.asarray(Cf).flatten()
    nan_ind = np.isnan(Cr) | np.isnan(Cf)
    Cr = Cr[~nan_ind]
    Cf = Cf[~nan_ind]
    
    mean_val = np.mean(Cf)
    std_val = np.std(Cf, ddof=1)
    rmsd = np.std(Cf - Cr, ddof=1)
    cor = np.corrcoef(Cf, Cr)[0, 1]
    return np.array([mean_val, std_val, rmsd, cor])

def draw_taylor_axes(ax, ref_std, s_lim, title, max_rmsd, hide_xlabel=False, hide_ylabel=False):
    ax.set_xlim(0, s_lim * 1.18)
    ax.set_ylim(0, s_lim * 1.18)
    ax.set_aspect('equal')
    
    ax.set_facecolor('white')
    
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('k')
        spine.set_linewidth(1.0)
    
    title_height = 0.12
    rect = Rectangle((0, 1.0), 1.0, title_height, transform=ax.transAxes, 
                     facecolor=[253/255, 228/255, 203/255], edgecolor='k', clip_on=False, linewidth=1.0)
    ax.add_patch(rect)
    ax.text(0.5, 1.0 + title_height/2, title, transform=ax.transAxes, 
            ha='center', va='center', fontsize=18, fontname='Times New Roman')
            
    ax.set_xticks([])
    ax.set_yticks([])
    
    locator = ticker.MaxNLocator(nbins=6, steps=[1, 2, 2.5, 5, 10])
    std_ticks = locator.tick_values(0, s_lim)
    std_ticks = std_ticks[(std_ticks > 0) & (std_ticks <= s_lim)]
    
    s_minor_ticks = []
    if len(std_ticks) >= 2:
        step = std_ticks[1] - std_ticks[0]
        minor_step = step / 5.0
        s_minor_ticks = np.arange(minor_step, s_lim, minor_step)
        s_minor_ticks = [x for x in s_minor_ticks if not any(np.isclose(x, t) for t in std_ticks)]
        
    for r in std_ticks:
        arc = Arc((0, 0), 2*r, 2*r, theta1=0, theta2=90, color='k', linewidth=0.5)
        ax.add_patch(arc)
        
        ax.plot([r, r], [0, s_lim*0.015], color='k', linewidth=0.8)
        ax.plot([0, s_lim*0.015], [r, r], color='k', linewidth=0.8)
        
        if not hide_xlabel:
            ax.text(r, -s_lim*0.03, f"{r:g}", ha='center', va='top', fontname='Times New Roman', fontsize=12)
        if not hide_ylabel:
            ax.text(-s_lim*0.03, r, f"{r:g} ", ha='right', va='center', fontname='Times New Roman', fontsize=12)
            
    for r in s_minor_ticks:
        ax.plot([r, r], [0, s_lim*0.008], color='k', linewidth=0.8)
        ax.plot([0, s_lim*0.008], [r, r], color='k', linewidth=0.8)

    ax.plot([0, s_lim], [0, 0], color='k', linewidth=1.2)
    ax.plot([0, 0], [0, s_lim], color='k', linewidth=1.2)
    
    c_tick_values = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
    c_minor_values = [0.05, 0.15, 0.2, 0.25, 0.35, 0.4, 0.45, 0.55, 0.6, 0.65, 0.75, 0.8, 0.85, 0.91, 0.92, 0.93, 0.94, 0.96, 0.97, 0.98, 1.0]
    
    for c in c_tick_values:
        angle = np.arccos(c)
        x = s_lim * np.cos(angle)
        y = s_lim * np.sin(angle)
        
        # 灰色放射线
        ax.plot([0, x], [0, y], color=[0.8, 0.8, 0.8], linestyle='-', linewidth=0.5)
        
        # 黑色刻度线向内
        tick_len = s_lim * 0.02
        ax.plot([x, x - tick_len*np.cos(angle)], [y, y - tick_len*np.sin(angle)], color='k', linewidth=1.0)
        
        # 径向刻度文字放回外侧，紧贴着黑弧
        padding = s_lim * 0.02
        ax.text(x + padding*np.cos(angle), y + padding*np.sin(angle), f"{c:g}", 
                ha='left', va='center_baseline', fontname='Times New Roman', fontsize=12, 
                rotation=np.degrees(angle), rotation_mode='anchor')
        
    for c in c_minor_values:
        angle = np.arccos(c)
        x = s_lim * np.cos(angle)
        y = s_lim * np.sin(angle)
        tick_len = s_lim * 0.01
        ax.plot([x, x - tick_len*np.cos(angle)], [y, y - tick_len*np.sin(angle)], color='k', linewidth=0.8)

    # 保持 Correlation 在原处，呈切线排列（即沿45度外缘切过），适度增加与坐标轴的距离
    lbl_dist = s_lim * 1.15
    x_cor = lbl_dist * np.cos(np.pi/4)
    y_cor = lbl_dist * np.sin(np.pi/4)
    ax.text(x_cor, y_cor, 'Correlation', ha='center', va='center', fontname='Times New Roman', fontsize=14, rotation=-45)
    
    # 仅仅升高 RMS error，使其远远避开 Correlation
    ax.text(x_cor, y_cor + s_lim * 0.23, 'RMS error', color=[0.77, 0.6, 0.18], ha='center', va='center', fontname='Times New Roman', fontsize=14, fontweight='bold', rotation=0)
            
    arc_outer = Arc((0, 0), 2*s_lim, 2*s_lim, theta1=0, theta2=90, color='k', linewidth=1.2)
    ax.add_patch(arc_outer)
    
    # 过滤掉远大于 max_rmsd 的无用刻度线
    if len(std_ticks) >= 2:
        step = std_ticks[1] - std_ticks[0]
        rmsd_ticks = [r for r in std_ticks if r <= max_rmsd + step * 0.5]
    else:
        rmsd_ticks = std_ticks
        
    for r in rmsd_ticks:
        t = np.linspace(0, np.pi, 200)
        rx = ref_std + r * np.cos(t)
        ry = r * np.sin(t)
        
        dist_from_origin = np.sqrt(rx**2 + ry**2)
        valid = (ry >= 0) & (dist_from_origin <= s_lim)
        
        ax.plot(rx[valid], ry[valid], color=[0.77, 0.6, 0.18], linestyle='--', linewidth=1.2)
        
        lbl_angle = 5 * np.pi / 6
        lx = ref_std + r * np.cos(lbl_angle)
        ly = r * np.sin(lbl_angle)
        if np.sqrt(lx**2 + ly**2) <= s_lim and ly >= 0:
            ax.text(lx, ly, f"{r:g}", ha='center', va='bottom', fontname='Times New Roman', fontsize=12, color=[0.77, 0.6, 0.18], fontweight='bold', rotation=60)

def main():
    data = pd.read_csv('Python/data.csv', header=None).values
    ref_data = data[:, 0]
    num_models = data.shape[1] - 1
    
    STATS = np.zeros((4, num_models))
    for i in range(num_models):
        STATS[:, i] = SStats(ref_data, data[:, i + 1])
        
    ref_std = np.std(ref_data, ddof=1)
    stds = STATS[1, :]
    cors = STATS[3, :]
    
    s_lim = max(np.max(stds), ref_std) * 1.15

    fig = plt.figure(figsize=(10, 8))
    fig.patch.set_facecolor('white')
    
    gs = GridSpec(2, 2, figure=fig, left=0.12, right=0.76, bottom=0.10, top=0.948, wspace=0.0, hspace=0.12)
    
    ax3 = fig.add_subplot(gs[0, 0])
    ax4 = fig.add_subplot(gs[0, 1])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    
    fig.text(0.44, 0.02, r"Standard Deviation(mm month$^{-1}$)", ha='center', va='bottom', fontsize=18, fontname='Times New Roman')
    fig.text(0.04, 0.524, r"Standard Deviation(mm month$^{-1}$)", ha='center', va='center', rotation=90, fontsize=18, fontname='Times New Roman')
    
    axes_list = [ax1, ax2, ax3, ax4]
    hide_x_flags = [False, False, True, True]
    hide_y_flags = [False, True, False, True]
    titles = ['Autumn', 'Winter', 'Spring', 'Summer']
    
    colorsList = np.array([
        [145, 81, 155], [217, 34, 30], [68, 127, 183], 
        [76, 181, 75], [145, 81, 155], [248, 130, 7]
    ]) / 255.0
    
    labels = ['# 1 1/x', '# 2 e^-x(x/0.1^2)', '# 3 e^-x(x/0.5^2)', '# 4 e^-x(x/0.2^2)', '# 5 e^-x(x/0.25^2)']
    scatter_handles = []
    
    # max_rmsd across all models
    max_rmsd = np.max(STATS[2, :])
    
    for idx, ax in enumerate(axes_list):
        draw_taylor_axes(ax, ref_std, s_lim, titles[idx], max_rmsd, hide_xlabel=hide_x_flags[idx], hide_ylabel=hide_y_flags[idx])
        
        ax.scatter(ref_std, 0, marker='o', s=80, facecolors=colorsList[0], edgecolors=colorsList[0], zorder=5, clip_on=False)
        ax.text(ref_std, s_lim*0.04, 'observed', ha='center', va='bottom', color=colorsList[0], fontweight='bold', fontsize=12, fontname='Times New Roman')
        
        for i in range(num_models):
            c = colorsList[i+1]
            x = stds[i] * np.cos(np.arccos(cors[i]))
            y = stds[i] * np.sin(np.arccos(cors[i]))
            
            sc = ax.scatter(x, y, marker='o', s=80, facecolors=c, edgecolors=c, zorder=5)
            if idx == 3:
                scatter_handles.append(sc)

    lgd = fig.legend(scatter_handles, labels, loc='center left', bbox_to_anchor=(0.765, 0.524), 
                     frameon=False, prop={'family': 'Times New Roman', 'size': 12})
    lgd.set_title('Weighting Scheme', prop={'family': 'Times New Roman', 'size': 14})

    plt.savefig('Python/result.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    main()
