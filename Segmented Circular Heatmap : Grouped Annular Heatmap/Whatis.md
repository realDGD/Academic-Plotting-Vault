### 🎯 模板标准命名

**分段环形热图 / 分组多环热力图 (Segmented Circular Heatmap / Grouped Annular Heatmap)**

### 🏷️ AI 检索高频关键词 (Tags)

建议使用这些中英双语的结构性术语作为标签，涵盖其几何特征与视觉逻辑：

- **基础图形**: 分段环形热图, 分组扇形热图, 极坐标矩阵图, segmented circular heatmap, grouped annular heatmap, polar correlation plot.
- **布局与拓扑**: 同心圆环 (concentric rings), 扇形分区 (sector partitioning), 物理间隙 (angular gaps), 中心留白 (center hole).
- **视觉细节**: 数值文本叠加 (text overlay), 阈值显著性高亮 (threshold significance highlighting/black bounding box), 外缘分类弧带 (outer category arcs), 径向旋转文本 (radial text rotation).
- **适用场景**: 多组分多维环境因子分析 (multi-group environmental factors), 模块化相关性矩阵 (modular correlation matrix).

### 📝 核心特征描述 (Prompt 提示词模板)

直接复制这段描述作为该模板的 AI 提示词。这段话精准剥离了具体的环境或土壤数据，提炼了复刻该图表所需的拓扑规则：

> “这是一个**基于极坐标的多分组分段环形热图 (Segmented Circular Heatmap)**。 **主体视觉**是由若干个带物理间隙的扇形区块组成的同心圆环阵列，单元格的颜色映射矩阵数值，且格内叠加显示具体数字。**阈值逻辑**：达到设定阈值（如绝对值>0.35）的单元格带有粗黑边框作为显著性高亮。 **外围与中心视觉**：图表中心留白放置全局标题；每个扇形区块的内外缘分别对齐径向旋转的行列变量标签；图表最外围由分段弧形带包裹，用于标识各个扇形区块的大类名称。底部配有独立的水平连续型颜色条。”

### 🗂️ 结构化特征解析 (模板属性卡片)

| **核心组件**            | **绘图类型与视觉特征**                                       |
| ----------------------- | ------------------------------------------------------------ |
| **整体布局 (Layout)**   | **分段极坐标系**。通过三角函数运算，将多个大小不一的矩阵映射为独立扇区，各组别之间依据预设比例（`sepRatio`）留有空白间隙（Gaps），使图表模块化。 |
| **主体视觉 (Heatmap)**  | **带文本与描边的多边形网格**。使用 `fill` 循环绘制网格；每个格内通过 `text` 居中显示数值；结合 `if-else` 逻辑判断，对超出设定阈值范围的极值网格单独应用黑实线描边（Highlighting），普通网格使用白线分隔。 |
| **标签与组别 (Labels)** | **径向文本与外围包裹带**。行列变量名分别贴合环形的内外边界；最外圈使用包含透明度（`EdgeAlpha`）的空白扇形块覆盖作为“大类指示带”，所有文本严格按所在极角动态计算 `Rotation`。 |
| **图例设计 (Legend)**   | **中心标题 + 底部色带**。中心预留出全图的最小半径圆心区放置大标题；底部使用独立坐标定位水平连续型 Colorbar。 |