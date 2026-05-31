# @author : slandarer (Translated to Python)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec

# 随机生成数据
np.random.seed(1)
part1 = np.linspace(-1, 2.5, 20).reshape(-1, 1) @ np.ones((1, 8))
part2 = np.linspace(0.5, -0.7, 20).reshape(-1, 1) @ np.ones((1, 5))
part3 = np.linspace(0.9, -0.2, 20).reshape(-1, 1) @ np.ones((1, 7))
offset = np.hstack([part1, part2, part3])
X = np.random.randn(20, 20) + offset
Y = X.copy()

# 计算数据相关性系数
Data = np.corrcoef(X.T)

# 输入行列名称
colName = ['FREM2','ALDH9A1','RBL1','AP2A2','HNRNPK','ATP1A1','ARPC3','SMG5','RPS27A',
          'RAB8A','SPARC','DDX3X','EEF1D','EEF1B2','RPS11','RPL13','RPL34','GCN1','FGG','CCT3']
rowName = colName.copy()
rowName = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14','A15']

# =========================================================================
# 获取数据矩阵大小
rows, cols = Data.shape

fig = plt.figure(figsize=(10, 8), facecolor='white')
fig.canvas.manager.set_window_title('slandarer')


# 坐标区域创建 =============================================================
gs = GridSpec(7, 9, figure=fig, 
              width_ratios=[1.2, 1, 1, 1, 1, 1, 1, 0.85, 0.25], 
              height_ratios=[1.2, 1, 1, 1, 1, 1, 1],
              wspace=0.05, hspace=0.05)

# 热图坐标区域
axMain = fig.add_subplot(gs[1:7, 1:7])
axMain.set_xlim(-0.5, cols - 0.5)
axMain.set_ylim(rows - 0.5, -0.5) # Equivalent to YDir='reverse'
axMain.set_xticks(np.arange(cols))
axMain.set_xticklabels(np.arange(1, cols + 1), rotation=45, ha='right', rotation_mode='anchor')
axMain.set_yticks(np.arange(rows))
axMain.set_yticklabels(np.arange(1, rows + 1))
axMain.tick_params(axis='x', bottom=False, top=False, labelbottom=True)
axMain.tick_params(axis='y', left=False, right=False, labelleft=False, labelright=True)

for spine in axMain.spines.values():
    spine.set_visible(False)

# 树状图坐标区域
axTree1 = fig.add_subplot(gs[1:7, 0])
axTree2 = fig.add_subplot(gs[0, 1:7])

# colorbar坐标区域
axBar = fig.add_subplot(gs[1:4, 8])

baseCM = np.array([
    [189, 53, 70],
    [255, 255, 255],
    [97, 97, 97]
]) / 255.0
cmap = LinearSegmentedColormap.from_list('custom_cmap', baseCM, N=200)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=1))
sm.set_array([])
CM = fig.colorbar(sm, cax=axBar)
CM.ax.tick_params(direction='in')

plt.savefig('untitled.png', dpi=300, bbox_inches='tight')
print("Image saved to untitled.png")
