### 🎯 模板标准命名

桑基-气泡组合图 / 分类流向与显著性对齐复合图 (Sankey-Bubble Composite Plot / Flow-Scatter Aligned Chart)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的专业术语作为标签保存，它们精准覆盖了该图表的几何联动和视觉特征：

- **基础图形** : 桑基图 (Sankey diagram), 气泡图 (Bubble chart/plot), 冲积图 (Alluvial diagram), 复合图表 (Composite chart/plot).
- **版式布局** : 左右并排布局 (Side-by-side layout), 节点坐标提取 (Node coordinate extraction), 共享特征 Y 轴 / 严格水平对齐 (Shared Y-axis horizontal alignment).
- **视觉细节** : 数据流向连线 (Flow ribbons/links), 矩形节点/色块 (Node patches), 气泡面积映射 (Bubble size mapping), 连续型颜色映射 (Continuous color mapping), 气泡图例与颜色条组合 (Bubble legend & Colorbar).
- **适用场景** : 通路富集分析多维可视化 (Enrichment analysis), 组分溯源流向与终端节点多维评价指标联合展示.

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段描述作为该模板的 AI 提示词（Prompt）。这段话精准剥离了具体数据，提取了 AI 复刻该底层绘图逻辑所需的所有拓扑关系和对齐规则：

“这是一个**左右并排布局、在特定节点空间上实现水平对齐的画中画复合型图表**。**左侧面板**是一个桑基图 (Sankey Diagram)，用于展示多层级分类数据的流向关系与权重分配；**右侧面板**是一个气泡图 (Bubble Chart)。 **核心联动逻辑是**：通过代码提取左侧桑基图最右侧边缘一列节点（Patches）的 Y 轴坐标，计算其中点，并以此作为右侧对应气泡的 Y 轴坐标，从而实现桑基图流向终端与气泡图散点在视觉上的精确水平对齐。右侧气泡图的横坐标通常映射绝对数值（如 -Log P-value），气泡大小映射计数值（Count），气泡的填充颜色映射第三维度的比例或连续数值（如 Hit Ratio）。画布最右侧外侧布局有全局共享的颜色条（Colorbar）和气泡大小标尺（Bubble legend）。”
