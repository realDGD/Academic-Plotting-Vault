### 🎯 模板标准命名

**环形柱状图-核密度组合图 / 极坐标柱体与分布联动图 (Circular Bar Chart and KDE Composite Plot / Radial Bar & Density Dashboard)**

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的高频专业术语作为标签保存，精准覆盖它的底层绘制技巧与排版特征：

- **基础图形** : 环形柱状图 (Circular bar chart), 径向柱状图 (Radial bar chart), 核密度图 (Kernel density estimation plot / KDE), 面积图 (Area plot).
- **布局与拓扑** : 左右并排布局 (Side-by-side layout), 笛卡尔坐标模拟极坐标 (Cartesian simulation of polar coordinates), 画板拼接 (Dashboard/Composite chart).
- **视觉细节** : 同心环辅助网格 (Concentric ring grid), 半透明面积填充 (Translucent area fill / FaceAlpha), 垂直基准虚线 (Vertical dashed baseline), 自定义多边形图例 (Custom polygon legend patches), 径向文本对齐 (Radial text alignment).
- **适用场景** : 基因富集分析可视化 (Gene enrichment analysis), 个体特征与群体统计分布联合展示 (Joint display of individual values and overall distribution).

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段描述作为该模板的 AI 提示词（Prompt）。这段话剔除了具体的基因或测试数据，向 AI 精准下达了复刻该图表所需的拓扑结构和渲染指令：

> “这是一个左右并排布局的高级复合型图表。**左侧面板**是一个环形柱状图 (Circular Bar Chart)，其底层没有使用原生的极坐标系，而是利用三角函数在笛卡尔坐标系下绘制了同心圆网格和带有物理宽度的弯曲柱体，每个柱体外部带有对齐的文本标签；**右侧面板**是一个核密度分布图 (KDE Plot)，利用半透明填充的面积图展示了多组数据的分布曲线，并包含一根垂直虚线作为辅助基准。整个画布左右两部分共享同一套分类配色方案，并通过自定义的多边形图例进行说明。”
