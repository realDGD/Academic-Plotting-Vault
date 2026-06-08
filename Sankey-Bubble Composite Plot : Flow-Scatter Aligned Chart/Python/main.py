"""
图表：桑基-气泡组合图 / 分类流向与显著性对齐复合图 (Sankey-Bubble Composite Plot)
依赖：matplotlib, pandas, numpy
数据输入：data_sankey.csv, data_bubble.csv
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches
import os

# Original image matched colors
group_colors = {
    'A': '#78335D', # Purple
    'B': '#9E5030', # Brown
    'C': '#C79A3A', # Gold
    'D': '#DFDE7E', # Yellow-green
    'E': '#A6E0C5', # Light green
    'F': '#61B5D4', # Light blue
    'G': '#4B6CA6', # Dark blue
    'H': '#6D3865'  # Purple-dark
}

def create_sankey_bubble_plot():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    df_sankey = pd.read_csv(os.path.join(script_dir, 'data_sankey.csv'))
    df_bubble = pd.read_csv(os.path.join(script_dir, 'data_bubble.csv'))

    fig = plt.figure(figsize=(12, 14), facecolor='white')
    
    # 1. Prepare data for Sankey
    sources = []
    for c in 'abcdefgh':
        for i in range(1, 6):
            if f"{c}{i}" in df_sankey['source'].values:
                sources.append(f"{c}{i}")

    for s in df_sankey['source'].unique():
        if s not in sources:
            sources.append(s)
            
    targets = list('ABCDEFGH')

    links = df_sankey.to_dict('records')
    source_links = {s: [] for s in sources}
    target_links = {t: [] for t in targets}
    for l in links:
        source_links[l['source']].append(l)
        target_links[l['target']].append(l)
        
    source_totals = {s: sum(l['value'] for l in source_links[s]) for s in sources}
    target_totals = {t: sum(l['value'] for l in target_links[t]) for t in targets}

    total_val = sum(source_totals.values())
    target_gap_min = total_val * 0.04
    required_target_span = total_val + 7 * target_gap_min
    
    # We want required_target_span to be exactly 2/3 of H
    H_target = required_target_span * 1.5
    total_left_gaps = H_target - total_val
    
    num_group_gaps = 0
    num_node_gaps = 0
    for i in range(len(sources) - 1):
        if sources[i][0] != sources[i+1][0]:
            num_group_gaps += 1
        else:
            num_node_gaps += 1
            
    node_gap = total_left_gaps / (num_node_gaps + num_group_gaps)
    group_gap = node_gap

    source_y = {}
    current_y = 0
    for i, s in enumerate(sources):
        source_y[s] = current_y
        current_y += source_totals[s]
        if i < len(sources) - 1:
            next_s = sources[i+1]
            if s[0] != next_s[0]:
                current_y += group_gap
            else:
                current_y += node_gap

    H = current_y + source_totals[sources[-1]] if sources else 0
    
    # Right nodes Y (2/3 of H, bottom aligned!)
    target_span = H * (2.0 / 3.0)
    start_right = H - target_span
    end_right = H
    
    total_val_right = sum(target_totals[t] for t in targets)
    target_gap = (target_span - total_val_right) / (len(targets) - 1) if len(targets) > 1 else 0

    target_y = {}
    current_y = start_right
    for t in targets:
        target_y[t] = current_y
        current_y += target_totals[t] + target_gap

    for t in targets:
        target_links[t].sort(key=lambda l: source_y[l['source']])

    # Physical layout mapping
    pad = H * 0.02
    ax1_y_min = -pad
    ax1_y_max = H + pad
    D = ax1_y_max - ax1_y_min

    ax1_bottom = 0.1
    ax1_height = 0.8
    # Expand ax1 width to increase horizontal space inside Sankey
    ax1 = fig.add_axes([0.05, ax1_bottom, 0.48, ax1_height])

    def get_phys_y(y_data):
        return ax1_bottom + ax1_height * (ax1_y_max - y_data) / D

    # ax2 EXACTLY matches the top of A and bottom of H
    ax2_y_min = start_right
    ax2_y_max = end_right

    ax2_phys_bottom = get_phys_y(ax2_y_max)
    ax2_phys_top = get_phys_y(ax2_y_min)
    ax2_phys_height = ax2_phys_top - ax2_phys_bottom

    # Move ax2 closer to ax1 right edge, make it wider
    ax2 = fig.add_axes([0.535, ax2_phys_bottom, 0.26, ax2_phys_height])

    # Draw Sankey Nodes
    node_width = 0.15 # Reduced width (3/4 of 0.2)
    right_x = 3.0 # Increased distance between left and right nodes
    
    for s in sources:
        y = source_y[s]
        h = source_totals[s]
        color = group_colors.get(s[0].upper(), '#333333')
        rect = patches.Rectangle((0, y), node_width, h, facecolor=color, edgecolor='none')
        ax1.add_patch(rect)
        ax1.text(-0.05, y + h/2, s, ha='right', va='center', fontsize=14, fontname='Times New Roman')

    target_mids = []
    for t in targets:
        y = target_y[t]
        h = target_totals[t]
        color = group_colors.get(t, '#333333')
        rect = patches.Rectangle((right_x-node_width, y), node_width, h, facecolor=color, edgecolor='none')
        ax1.add_patch(rect)
        ax1.text(right_x-node_width - 0.05, y + h/2, t, ha='right', va='center', fontsize=18, fontname='Times New Roman')
        target_mids.append(y + h/2)

    # Draw Ribbons
    source_curr_y = {s: source_y[s] for s in sources}
    target_curr_y = {t: target_y[t] for t in targets}

    for t in targets:
        for l in target_links[t]:
            s = l['source']
            v = l['value']
            
            y0_upper = source_curr_y[s]
            y0_lower = y0_upper + v
            y1_upper = target_curr_y[t]
            y1_lower = y1_upper + v
            
            source_curr_y[s] += v
            target_curr_y[t] += v
            
            x0 = node_width
            x1 = right_x - node_width
            mid_x = (x0 + x1) / 2
            
            verts = [(x0, y0_upper), (mid_x, y0_upper), (mid_x, y1_upper), (x1, y1_upper),
                     (x1, y1_lower), (mid_x, y1_lower), (mid_x, y0_lower), (x0, y0_lower), (x0, y0_upper)]
            codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.LINETO,
                     Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
            
            patch = patches.PathPatch(Path(verts, codes), facecolor='#E0E0E0', edgecolor='white', lw=0.5, alpha=0.7)
            ax1.add_patch(patch)

    ax1.set_xlim(-0.5, right_x + 0.02) # Tightly crop the right side to minimize gap to bubble chart
    ax1.set_ylim(ax1_y_max, ax1_y_min) 
    ax1.axis('off')

    # Bubble Chart
    ax2.set_ylim(ax2_y_max, ax2_y_min) # Exactly bounds A-H, no padding!
    c_low = (114/255, 164/255, 207/255)
    c_high = (4/255, 56/255, 86/255)
    cmap_blue = LinearSegmentedColormap.from_list('custom_blues', [c_low, c_high])
    bubble_scale = 280
    
    scatter = ax2.scatter(
        df_bubble['NLogPvalue'], 
        target_mids, 
        s=df_bubble['Count'] * bubble_scale, 
        c=df_bubble['HitRatio'], 
        cmap=cmap_blue, 
        vmin=0.15, vmax=0.45,
        alpha=0.9,
        edgecolors='none',
        clip_on=False # Prevent cutting off bubbles if they touch the spine
    )
    
    ax2.set_xlim(-0.6, 2.4)
    ax2.set_xticks([-0.5, 0, 0.5, 1, 1.5, 2])
    ax2.tick_params(axis='x', direction='out', labelsize=16, top=True, labeltop=False, bottom=True, labelbottom=True, length=6)
    ax2.tick_params(axis='y', left=False, labelleft=False)
    
    for spine in ax2.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color('black')
        
    ax2.set_xlabel('-Log(Pvalue)', fontsize=20, fontweight='bold', fontname='Times New Roman', labelpad=12)

    # Align Count and Hit Ratio Titles
    title_x = 0.83
    
    # Hit Ratio Section (moved to center of A node)
    A_mid_phys_y = get_phys_y(target_mids[0])
    fig.text(title_x, A_mid_phys_y, 'Hit Ratio', fontsize=20, fontweight='bold', fontname='Times New Roman', va='center')
    
    # Increase colorbar length, align left edge with bubbles
    cbar_x = 0.835
    cbar_h = ax2_phys_height * 0.45
    cbar_y = A_mid_phys_y - 0.03 - cbar_h
    cbar_ax = fig.add_axes([cbar_x, cbar_y, 0.02, cbar_h])
    
    # Explicitly set original ticks
    cb = fig.colorbar(scatter, cax=cbar_ax, ticks=[0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45])
    cb.outline.set_linewidth(1.5)
    cb.ax.tick_params(labelsize=14, direction='in')

    # Count Section
    count_title_y = ax2_phys_bottom + ax2_phys_height * 0.35
    fig.text(title_x, count_title_y, 'Count', fontsize=20, fontweight='bold', fontname='Times New Roman', va='center')
    
    ax_size_bottom = ax2_phys_bottom
    ax_size_height = count_title_y - 0.02 - ax_size_bottom
    ax_size = fig.add_axes([0.836, ax_size_bottom, 0.15, ax_size_height])
    ax_size.set_xlim(-0.5, 2.5)
    ax_size.set_ylim(0, 3.8)
    ax_size.set_xticks([])
    ax_size.set_yticks([])
    for spine in ax_size.spines.values():
        spine.set_visible(False)

    size_vals = [8 * bubble_scale, 5 * bubble_scale, 2 * bubble_scale]
    label_vals = [8, 5, 2]
    # Spread the bubbles a bit more and move them up
    y_positions = [3.2, 2.0, 0.8]

    ax_size.plot([0.8, 0.8], [0.8, 3.2], color='black', linewidth=1.2, zorder=1)
    
    for i, (sz, val, y_pos) in enumerate(zip(size_vals, label_vals, y_positions)):
        ax_size.scatter(0, y_pos, s=sz, facecolor='#666666', edgecolor='none', zorder=2, clip_on=False)
        if i != 1: # Only draw tick for max and min
            ax_size.plot([0.8, 1.0], [y_pos, y_pos], color='black', linewidth=1.2, zorder=1)
            ax_size.text(1.2, y_pos, f"{val}", va='center', ha='left', fontname='Times New Roman', fontsize=16)

    # Save
    out_file = os.path.join(script_dir, 'result.png')
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {out_file}")

if __name__ == '__main__':
    create_sankey_bubble_plot()
