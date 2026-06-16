"""
图表：Stacked Bar Chart with Connections : Alluvial-style Bar Chart
依赖：matplotlib, pandas, numpy
数据输入：data.csv，包含列名。第一列为行名，其余为各系列数据。
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Set current directory to file directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. 读取数据并预处理
df = pd.read_csv('data.csv')
row_names = df.iloc[:, 0].values
col_names = df.columns[1:].values
data = df.iloc[:, 1:].values

# 2. 修改柱状图配色
CList = np.array([
    [144, 170, 220],
    [169, 209, 143],
    [255, 231, 153],
    [219, 219, 219]
]) / 255.0

fig, ax = plt.subplots(figsize=(10, 8))

num_bars = data.shape[0]
num_series = data.shape[1]
x = np.arange(1, num_bars + 1)
bar_width = 0.65

# 计算每个bar的上下边界，用于绘制柱状图和连接多边形
y_end_points = np.zeros((num_series + 1, num_bars))
for i in range(num_series):
    y_end_points[i+1, :] = y_end_points[i, :] + data[:, i]

# 3. 绘制堆叠柱状图
for i in range(num_series):
    ax.bar(
        x, data[:, i], 
        bottom=y_end_points[i, :], 
        width=bar_width, 
        color=CList[i], 
        edgecolor='w', 
        linewidth=1,
        label=col_names[i]
    )

# 4. 绘制冲积图链接部分
alpha_val = 0.4
half_width = bar_width * 0.5

for i in range(num_series):
    for j in range(num_bars - 1):
        x_poly = [
            x[j] + half_width,
            x[j+1] - half_width,
            x[j+1] - half_width,
            x[j] + half_width
        ]
        y_poly = [
            y_end_points[i, j],
            y_end_points[i, j+1],
            y_end_points[i+1, j+1],
            y_end_points[i+1, j]
        ]
        
        ax.fill(
            x_poly, y_poly,
            color=CList[i],
            alpha=alpha_val,
            edgecolor='w',
            linewidth=1
        )

# 5. 坐标区域修饰
ax.set_xlim(0.5, num_bars + 0.5)
ax.set_ylim(-1, 100)
ax.set_xticks(x)
ax.set_xticklabels(row_names, fontsize=18)
ax.set_yticks(np.arange(0, 101, 25))
ax.set_yticklabels(np.arange(0, 101, 25), fontsize=18)
ax.set_ylabel('Explained variation(%)', fontsize=20)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.tick_params(axis='both', which='major', direction='out', length=6, width=2)

# 图例
ax.legend(
    loc='center left', 
    bbox_to_anchor=(1, 0.5),
    frameon=False,
    fontsize=14,
    handlelength=0.9,
    handleheight=0.9,
    handletextpad=0.5
)

plt.tight_layout()
plt.savefig('result.png', dpi=300)
