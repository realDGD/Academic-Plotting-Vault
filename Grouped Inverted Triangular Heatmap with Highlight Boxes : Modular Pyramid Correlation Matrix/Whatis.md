### 🎯 模板标准命名

带分组高亮边框的倒三角热图 / 模块化金字塔相关性矩阵 (Grouped Inverted Triangular Heatmap with Highlight Boxes / Modular Pyramid Correlation Matrix)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的高频专业术语作为标签保存，精准覆盖它的几何变换、聚类特征与高亮修饰：

- **基础图形**: 倒三角热图 (Inverted triangular heatmap), 金字塔热图 (Pyramid heatmap), 聚类相关性矩阵 (Clustered correlation matrix).
- **布局与拓扑**: -45度旋转 (-45 degree rotation), 下三角保留 (Lower-triangular retained), 层次聚类重排 (Hierarchical clustering reordering).
- **视觉细节**: 分组高亮边框 (Group highlight bounding boxes), 模块边界线 (Module boundary lines), 顶部斜交标签 (Top slanted labels).
- **适用场景**: 多组学特征模块化分析 (Modular analysis of multi-omics features), 复杂变量组内/组间共线性高亮可视化.

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段简短的描述作为该模板的 AI 提示词（Prompt）。这段话精准剥离了具体数据，向 AI 解释了其特殊的拓扑结构和高亮逻辑：

> “这是一个**带分组高亮边框的倒三角相关性热图**。主体视觉是一个倒置的金字塔形热图（通过对称矩阵旋转-45度并隐藏上半部分实现）。行列数据经过层次聚类重新排序，但**不显示边缘树状图**。其核心特征是：在热图表面叠加了根据聚类结果计算坐标的粗线条多边形边框（Highlight Boxes/Lines），用于显式地圈定和高亮特定的分类模块（如主对角线上的类簇区块），并在边缘添加了独立的大字号分组标签（如A、B）。”