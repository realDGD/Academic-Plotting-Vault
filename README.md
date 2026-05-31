# Python Painting Vault 🎨

通过 Python 尽可能高质量复刻「公众号：*slandarer随笔*」中的 MATLAB 绘图，相应的 MATLAB 原版代码请在其公众号获取。

个人的使用方式是跟 ai 对话，对话 prompt 示例：

```text
请先读取【填本项目位置】的 `ai_index.json` 文件，寻找适合画【输入你的数据场景，如：基因表达量】的图表。找到对应文件夹后，进入该文件夹阅读其内部的 `Whatis.md` 和 `Python/main.py`，最后根据我提供的新数据（数据文件（夹）为 【xxx】）修改代码，【数据文件的格式为 xxx（第一列是...第二列是...）】，代码和图片保存在数据文件夹处。整个过程请遵守 `AGENTS.md` 的全局规范。
```



---

## 🛠 运行环境与依赖 (Environment)

本仓库采用最前沿的 [uv](https://github.com/astral-sh/uv) 作为唯一的包管理器，完全隔离全局环境，告别依赖冲突。

### 1. 安装 uv
如果你还没有安装 `uv`，可以通过以下命令快速安装：
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 还原项目依赖 (安装)
克隆本项目后，**不需要**手动创建虚拟环境。直接在项目根目录下运行：
```bash
uv sync
```
*`uv` 会自动读取 `pyproject.toml` 和 `uv.lock`，在百毫秒级的时间内为你配置好完美的局部虚拟环境（包含 `pandas`, `matplotlib`, `seaborn`, `pyecharts` 等必要库）。*

### 3. 运行任意图表代码
所有图表的主运行程序统一为 `Python/main.py`。请使用 `uv run` 执行，它会自动使用局部环境：
```bash
# 进入你想要的图表目录
cd "Bipartite Chord Diagram : Circular Flow Chart"

# 运行画图脚本
uv run Python/main.py
```
*运行成功后，当前 `Python/` 目录下会生成名为 `result.png` 或 `result.html` 的最终渲染图。*

---

## 📁 目录结构 (Structure)

本仓库有着严格的组织规范，每一个图表都拥有独立的沙箱文件夹，结构如下：

```text
Python_Painting_Vault/
├── .envrc                 # 命令行自动载入环境（若无安装 direnv 请忽略）
├── pyproject.toml         # 核心依赖管理清单 (由 uv 维护)
├── uv.lock                # 环境锁文件，确保所有人的运行环境 100% 一致
├── build_index.py         # AI 索引及 README 目录自动生成脚本
├── ai_index.json          # 供大模型(AI)调库使用的全局检索字典
└── [图表名称文件夹]/        # 如: Bipartite Chord Diagram...
    ├── Whatis.md          # 记录图表特征、视觉细节、数据逻辑及关键词
    └── Python/
        ├── main.py        # Python 版本的绘图源码（统一入口）
        ├── data.csv       # 抽离的测试数据
        └── result.png     # Python 最终渲染生成的图片
```
*(注：对于开发者，私有仓库中额外包含 `AGENTS.md` 工作流规范及 `Matlab/` 原始对照文件。)*

---

## 🤖 自动化与 AI 工作流

本仓库深度融合了 AI 辅助工作流。
当仓库新增图表后，运行 `python3 build_index.py`。该脚本会自动更新供 AI 读取的 `ai_index.json`，并**自动将新图表追加到下方的图表大厅中**。

---

## 🖼 图表大厅 (Gallery)

目前能够绘制的高级图表有：

<!-- CHART_LIST_START -->
- **[Inset Composite Chart —— Line Plot with Horizontal Bar-Scatter](./Inset%20Composite%20Chart%20%E2%80%94%E2%80%94%20Line%20Plot%20with%20Horizontal%20Bar-Scatter)**
- **[Clustered Heatmap : Hierarchically Clustered Heatmap](./Clustered%20Heatmap%20%3A%20Hierarchically%20Clustered%20Heatmap)**
- **[Bipartite Chord Diagram : Circular Flow Chart](./Bipartite%20Chord%20Diagram%20%3A%20Circular%20Flow%20Chart)**
- **[Compact Dual-Panel Grouped Bar Chart](./Compact%20Dual-Panel%20Grouped%20Bar%20Chart)**

<!-- CHART_LIST_END -->
