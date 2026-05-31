### 🎯 模板标准命名

**画中画复合图：折线图嵌套水平柱点图 (Inset Composite Chart: Line Plot with Horizontal Bar-Scatter)**

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的专业术语直接作为标签保存，涵盖了所有的绘图难点和特征：

- **布局与结构:** 画中画, 嵌套子图, 复合图表, inset axes, nested subplots, picture-in-picture, shared global legend.
- **主图特征 (Main Plot):** 折线图带误差条, 背景高亮阴影, 垂直分隔线, line plot with error bars, shaded background area, vertical dashed separator.
- **子图特征 (Inset Plots):** 水平柱状图, 抖动散点图, 水平误差条, horizontal bar chart, jittered scatter plot, strip plot.
- **统计修饰:** 显著性标注, p值连线, custom legend patches, statistical significance brackets.

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段简短的描述作为该模板的 AI 提示词（Prompt）。当你想让 AI 复刻此类图形时，这段描述包含了所有必要的拓扑和视觉信息：

> “这是一个**画中画结构（Inset Axes）的复合型统计图**。 **主图**是一个带有垂直误差条的折线图，包含用于划分阶段的垂直虚线，以及一个自定义的背景灰色阴影区域。 **子图**：在主图的左上角和右上角悬浮嵌套了两个平行的子坐标系，子图类型为**带有水平误差条和抖动散点（Jittered Scatter）的水平柱状图**。 **全局特征**：所有图形共用一个位于顶部外侧（northoutside）的横向多列图例，并且主图与子图均带有自定义的统计学显著性连线和星号标注。”

### 🗂️ 结构化特征解析 (便于归档)

| **核心组件**                | **绘图类型与视觉特征**                                       |
| --------------------------- | ------------------------------------------------------------ |
| **主坐标系 (Bottom/Main)**  | **带误差的折线图**。特征：线宽较粗，节点带有实心圆点标记；包含利用 `fill` 绘制的底部灰色遮罩层（用于强调特定区间）。 |
| **嵌套坐标系 (Top Insets)** | **水平柱状图 + 抖动散点**。特征：利用绝对位置（Position）悬浮在主图上方；柱体无填充色（白色）加黑边，真实数据点以抖动（Jitter）形式叠加在对应的柱体上。 |
| **图例设计**                | 独立图例。未直接调用线条自身的图例，而是利用 `fill` 构建了自定义的色块（Patch）作为图例图标，全局居中置于画布顶部。 |
|                             |                                                              |