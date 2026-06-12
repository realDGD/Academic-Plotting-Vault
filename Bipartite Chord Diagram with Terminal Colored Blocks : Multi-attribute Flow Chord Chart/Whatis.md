### 🎯 模板标准命名

**末端独立着色的双边弦图 / 多维属性映射流向弦图** (Bipartite Chord Diagram with Terminal Colored Blocks / Multi-attribute Flow Chord Chart)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的专业术语作为标签保存，精准覆盖它的拓扑结构与高阶定制特征：

- **基础图形**: 弦图 (Chord diagram), 双边弦图 (Bipartite chord diagram/plot), 数据流向图 (Data flow chart), 关系网络图 (Relationship network plot).
- **布局与拓扑**: 圆形/极坐标布局 (Circular/polar layout), 上下半区映射 (Top-bottom hemisphere mapping), 来源-目标定向流 (Source-to-target directed flow).
- **视觉细节**: **弦末端独立着色 (Independent chord terminal coloring/blocks)**, 贝塞尔曲线带 (Bezier ribbons/bands), 径向自适应旋转标签 (Radial adaptive rotated labels), 半透明填充 (Translucent fill), 外置自定义图例 (Custom external legend).
- **适用场景**: 基因表达调控网络 (Gene expression regulation network), 多组学/组织靶向映射 (Multi-omics/tissue-target mapping), 带附加分类属性的转移矩阵展示.

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段话作为该模板的底层 AI 提示词（Prompt）。这段描述剥离了具体的肺、脾或基因数据，提炼了复刻该图表所需的最核心渲染逻辑：

> “这是一个**极坐标布局的双边弦图 (Bipartite Chord Diagram)**。图表呈圆形结构，明确区分为‘来源（下方弧段）’与‘目标（上方弧段）’两个半区。主体视觉由连接上下半区的半透明贝塞尔曲线（弦）构成，映射两组实体间的流量关系。
>
> **其核心高阶特征是‘弦末端方块独立着色’**：在每根弦流入目标弧段的末端，设有一个独立的小弧形色块，该色块的颜色与弦的主体颜色不同，用于映射第三维度的离散分类变量（如上调/下调）。此外，图表外围环绕着根据角度自适应旋转的文本标签，并在画布角落配有用于解释末端分类色块的图例。”
