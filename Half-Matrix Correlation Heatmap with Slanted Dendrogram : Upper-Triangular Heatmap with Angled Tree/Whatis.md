### 🎯 模板标准命名

带倾斜树状图的半角相关性热图 / 斜交树状图上三角热图 (Half-Matrix Correlation Heatmap with Slanted Dendrogram / Upper-Triangular Heatmap with Angled Tree)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的高频专业术语作为标签保存，精准覆盖该图表的几何变换与排版特征：

- **基础图形** : 半角热图 (Half-matrix heatmap), 上三角热图 (Upper-triangular heatmap), 相关性矩阵图 (Correlation matrix plot), 聚类热图 (Clustered heatmap).
- **布局与拓扑** : 倾斜树状图 (Slanted dendrogram / Angled cluster tree), -45度几何旋转 (-45 degree rotation), 下三角隐藏/遮盖 (Lower-triangular cleared/hidden), 斜交对齐 (Diagonal/oblique alignment).
- **视觉细节** : 连续型颜色条 (Continuous colorbar), 隐藏坐标轴线 (Hidden axes lines/XColor none).
- **适用场景** : 多组学特征共线性分析 (Multi-omics collinearity analysis), 冗余对称矩阵的空间压缩可视化.

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段简短的描述作为该模板的 AI 提示词（Prompt）。这段话剔除了具体数据，向 AI 精准下达了复刻该图表所需的底层几何变换与遮罩逻辑：

> “这是一个**带倾斜聚类树状图的半角复合相关性热图 (Upper-Triangular Heatmap with Slanted Dendrogram)**。主体部分是一个相关性矩阵热图，但通过代码隐藏了它的下三角部分（下三角单元格不可见），仅保留上三角矩阵结构；其最核心的视觉特征是：左侧边缘的层次聚类树状图（Dendrogram）被整体旋转了 -45 度，以斜交的姿态放置，与右侧的行文本标签遥相呼应。图表去除了传统的 XY 坐标轴网格线，并在底部外侧居中放置了一个水平颜色条 (Colorbar)。”