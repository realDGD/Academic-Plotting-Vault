### 🎯 模板标准命名

**带分组树状图的倒三角相关性热图 / 分类金字塔聚类热图** *(Inverted Triangular Correlation Heatmap with Grouped Dendrogram / Pyramid Clustered Heatmap)*

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的高频专业术语作为标签保存，精准覆盖该图表的几何变换、空间排版与聚类特征：

- **基础图形**: 倒三角热图 (Inverted triangular heatmap), 金字塔热图 (Pyramid heatmap), 聚类热图 (Clustered heatmap), 相关性矩阵 (Correlation matrix).
- **布局与拓扑**: -45度旋转 (-45 degree rotation), 下三角矩阵保留 (Lower-triangular retained), 边缘对齐 (Marginal alignment), 空间压缩 (Space compression).
- **视觉细节**: 层次聚类树状图 (Hierarchical clustering dendrogram), 分组着色树枝 (Color-coded dendrogram branches), 类间物理间隙 (Cluster gaps/Separation gaps), 45度倾斜标签 (45-degree slanted labels).
- **适用场景**: 多变量共线性分析 (Multicollinearity analysis), 组学特征相互作用网络 (Omics feature interaction), 大规模对称数据降维展示。

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段话作为该模板的核心提示词，它精准剥离了具体数据，向 AI 下达了重构该图表所需的所有底层几何指令：

> “这是一个**带边缘分组树状图的倒三角复合聚类热图 (Inverted Triangular Clustered Heatmap)**。图表主体是一个通过对齐下三角矩阵并整体进行 -45 度旋转所形成的倒三角形（金字塔形）热图，用于展示对称数据的相关性以节省排版空间。热图的左上方（或左侧）完美对齐了一个对应的**层次聚类树状图 (Dendrogram)**。聚类树与热图网格不仅在节点上严格对应，并且根据聚类结果（MaxClust）划分了不同的颜色组，组与组之间通过插入空白的**物理间隙 (Cluster Gaps)** 进行了视觉隔离。变量文本标签沿着倒三角的斜边以 45 度角倾斜排列。”