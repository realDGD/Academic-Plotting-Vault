# @author : slandarer (Translated to Python)
# 公众号  : slandarer随笔
# 知乎    : slandarer

import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
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
# X=randn(20,15)+[(linspace(-1,2.5,20)').*ones(1,4),(linspace(.5,-.7,20)').*ones(1,5),(linspace(.9,-.2,20)').*ones(1,6)];

# 计算数据相关性系数
Data = np.corrcoef(X.T)

# 输入行列名称
colName = ['FREM2','ALDH9A1','RBL1','AP2A2','HNRNPK','ATP1A1','ARPC3','SMG5','RPS27A',
          'RAB8A','SPARC','DDX3X','EEF1D','EEF1B2','RPS11','RPL13','RPL34','GCN1','FGG','CCT3']
rowName = colName.copy()
# rowName={'A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14','A15'};

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

# 树状图坐标区域
axTree1 = fig.add_subplot(gs[1:7, 0])
axTree2 = fig.add_subplot(gs[0, 1:7])

# colorbar坐标区域
axBar = fig.add_subplot(gs[1:4, 8])

# 图像绘制 =================================================================
# 绘制左侧树状图
tree1 = sch.linkage(Data, method='average')
sch.set_link_color_palette(['black'])
plt.rcParams['lines.linewidth'] = 1.0
dendro1 = sch.dendrogram(tree1, ax=axTree1, orientation='left', color_threshold=0, above_threshold_color='black')
axTree1.axis('off')
axTree1.set_ylim(0, rows * 10)
axTree1.invert_yaxis()

# 绘制上方树状图
tree2 = sch.linkage(Data.T, method='average')
dendro2 = sch.dendrogram(tree2, ax=axTree2, orientation='top', color_threshold=0, above_threshold_color='black')
axTree2.axis('off')
axTree2.set_xlim(0, cols * 10)

# 绘制中央热图
order1 = dendro1['leaves']
order2 = dendro2['leaves']

Data_ordered = Data[order1, :]
Data_ordered = Data_ordered[:, order2]

# 调整colorbar
# 这里对应 MATLAB 中 baseCM{1}
baseCM = np.array([
    [189, 53, 70],
    [255, 255, 255],
    [97, 97, 97]
]) / 255.0
cmap = LinearSegmentedColormap.from_list('custom_cmap', baseCM, N=200)

im = axMain.imshow(Data_ordered, aspect='auto', cmap=cmap, vmin=np.min(Data), vmax=np.max(Data))

axMain.set_xticks(np.arange(cols))
axMain.set_yticks(np.arange(rows))
axMain.set_xticklabels([colName[i] for i in order2], rotation=45, ha='right', rotation_mode='anchor')
axMain.set_yticklabels([rowName[i] for i in order1])
axMain.tick_params(axis='x', bottom=False, top=False, labelbottom=True)
axMain.tick_params(axis='y', left=False, right=False, labelleft=False, labelright=True)

for spine in axMain.spines.values():
    spine.set_visible(False)

# 绘制白线
for i in range(rows + 1):
    axMain.axhline(i - 0.5, color='white', linewidth=1)
for i in range(cols + 1):
    axMain.axvline(i - 0.5, color='white', linewidth=1)
    
axMain.set_xlim(-0.5, cols - 0.5)
axMain.set_ylim(rows - 0.5, -0.5)

CM = fig.colorbar(im, cax=axBar)
CM.ax.tick_params(direction='in')

# 工具函数 =================================================================
# 复制坐标区域全部图形对象
# (Skipped: Python handles axes creation directly via GridSpec)
# def copyAxes(fig, k, newAx):
#     pass

plt.savefig('treeHeatmapDemo.png', dpi=300, bbox_inches='tight')
print("Image saved to treeHeatmapDemo.png")
