### 🎯 模板标准命名

**带连接带的堆叠柱状图 / 冲积式柱状图 (Stacked Bar Chart with Connections / Alluvial-style Bar Chart)**

### 🏷️ AI 检索高频关键词 (Tags)

建议使用这些中英双语的高频术语作为标签，它们精准覆盖了该图表的几何联动和排版特征：

- **基础图形**: 堆叠柱状图 (Stacked bar chart), 冲积图 (Alluvial diagram), 连线柱状图 (Connected bar chart), flow bar chart.
- **版式布局**: 连续分类对比 (Sequential categorical comparison), 状态流转映射 (State transition mapping).
- **视觉细节**: 相邻柱体连接带/多边形连接 (Connecting bands / polygon connections), 半透明填充连线 (Semi-transparent fill links), 隐藏基线 (Hidden baseline), 图例分离 (External legend).
- **适用场景**: 组分占比随时间/空间/实验条件的动态变化追踪 (Tracking composition changes across conditions), 解释率/方差分解的可视化表现 (Visualizing explained variation).

### 📝 核心特征描述 (Prompt 提示词模板)

建议直接复制这段描述作为该模板的 AI 提示词（Prompt），它向 AI 解释了如何通过基础几何图形组合出这种高级效果：

> “这是一个**带连线带的冲积式堆叠柱状图 (Alluvial-style Stacked Bar Chart)**。其基础结构是一个常规的堆叠柱状图 (Stacked Bar)，用于展示各个分组的组分构成。核心视觉特征在于：**在相邻的柱体之间，使用与对应类别同色且带有半透明透明度（Alpha）的多边形色块（Polygons）将相同的层级连接起来**，形成类似冲积图（Alluvial diagram）的数据流向视觉效果。该图表非常适合展现多类别组分随横坐标（如不同站点、不同处理条件）的动态演变规律。”
