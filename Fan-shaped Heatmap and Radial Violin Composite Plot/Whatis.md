### 🎯 模板标准命名

**扇形热图-径向小提琴组合图 / 极坐标时序分布复合图 (Fan-shaped Heatmap and Radial Violin Composite Plot)**

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的专业术语作为标签保存，精准覆盖它的底层绘制技巧与视觉特征：

- **基础图形** : 扇形热图 (Fan-shaped heatmap), 环形/半环形热图 (Annular/Semi-circular heatmap), 径向小提琴图 (Radial violin plot), 极坐标复合图表 (Polar composite plot).
- **布局与拓扑** : 笛卡尔坐标系下的极坐标映射 (Cartesian-to-polar mapping), 扇形分区 (Sector partitioning), 径向延伸与对齐 (Radial outward alignment), 角度切割 (Angular slicing).
- **视觉细节** : 多边形填充热图网格 (Polygon-filled heatmap grid), 径向旋转文本 (Radial text rotation), 组合坐标轴/放射状辅助线 (Radial grid lines), 内部四分位线标注 (Inner quartile lines).
- **适用场景** : 周期性/季节性时序数据分析 (Periodic/seasonal time-series analysis), 宏观统计量与底层分布联合展示 (Joint display of macroscopic statistics and underlying distribution).

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段描述作为该模板的 AI 提示词（Prompt）。这段话剔除了具体的“日期”、“年月”等业务数据，提取了复刻该图表所需的所有核心几何映射规则：

> “这是一个基于笛卡尔坐标系通过三角函数手动映射构建的**极坐标复合图表**。该图表仅占据上半圆的特定扇形区域（如 150° 到 30°）。图表由内外两部分在径向上严格对齐组成：**内部**是一个由多边形网格构成的**扇形热图（Fan-shaped Heatmap）**，用于映射二维矩阵数据的数值；**外部**外接了一组**沿径向向外延伸的径向小提琴图（Radial Violin Plot）**，用于展示对应角度维度上的底层数据分布，小提琴图内部带有中位线和四分位线。最外侧带有依据角度旋转的文本标签，左侧/右侧带有斜向的分类标签。”
