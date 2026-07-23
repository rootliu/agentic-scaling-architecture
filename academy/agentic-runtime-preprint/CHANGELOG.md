# CHANGELOG

## v6 — 2026-07-23

审查方式：本机 v5 PDF 与从 GitHub 拉取的 obsidian/architecture 仓库最新内容逐条比对；聚焦图表引用准确性与行文流畅度。

### 图表 / 引用修正（6 处）

- **§3.2 / §8.4 陈旧交叉引用**：`Section~4.3` → `Section~5.3`（四条假设实际在 §5.3 "Conditional Decoupling"）；`Section~6.1` → `Section~7.1`（frozen prefix 概念实际在 §7.1）。
- **Figure 7 证伪矩阵缺行**：脚本 `_draw_evaluation_matrix` 的 `rows` 列表只有 8 行，缺 §9.4 "Control-Plane Leakage" 对应行（caption 已声明九行）；补齐后图高从 190pt 调整为 250pt 以消除溢出。
- **`\S` / `\Sigma` 替换冲突**：`latex_to_preprint.py` 的裸子串替换 `text.replace(r"\S", "Section")` 会误伤 `\Sigma`（渲染为 "Sectionigma"）；改为 `re.sub(r"\\S(?![a-zA-Z])", ...)`。
- **`\big(` / `\big[` 未处理**：脚本只处理了 `\bigl/\bigr/\Bigl/\Bigr`，论文正文的裸 `\big(`/`\big)`/`\big[`/`\big]`（§8.5 公式）落入通用反斜杠剥离兜底逻辑，融合成 "r_dbig(...)"；补充对应正则。
- **相邻希腊字母宏融合**：`\lambda\rho`、`\mu\bar{c}` 渲染为 "lambdarho"/"mubarc"；新增相邻反斜杠命令间插入空格的预处理，并为 `\lambda`/`\mu`/`\bar{}` 补充替换规则。

### 行文修订

- 全文 24 处 em-dash（`---`）短语堆砌句改写为通顺连接句（改用冒号、分号、"that is"、"such as"、"comprising" 等），保留全部引用、命题编号与章节交叉引用不变。

### 渲染 bug 修复

- `latex_to_preprint.py` 中 `text.replace("--", " - ")` 把合法的英文连字符范围（`(1)--(4)`、`data--output`、`5--20 nodes`、`human--agent`）渲染成带空格的短横线；改为 `text.replace("--", "-")`（`---` 仍按加空格短横处理，`--` 直接收紧）。

## v5 — 2026-07-22

将 vault 两篇最新研究笔记（`12-Skill作为可训练激活层-双子目标Reward`、`13-DataWiki-ThemeWiki-IR中间关系层`）的内容吸收进论文。无新增引用（仅用已有 [2] Chen et al. 与 [20] SkillOpt）；未声称任何实验结果。

### 内容修改

1. **新增 §8.5 "Training Before Freezing: A Dual-Subgoal Reward"**（接 §8.4 Skill-as-Code）：SkillOpt [20] 的单 scalar reward 是其自认局限；本文把 reward 结构化为结果子目标 r_out（沿 σ_out 子域各配独立标注 benchmark 加权）× 过程子目标 r_proc（工具/数据源/逻辑判据/step gate 的稠密即时信号），双维结构化 gate 记录带维度的负反馈；人工角色从每轮判断降为一次性确认评测方法；收敛子目标进入 freeze-to-code——train 与 compile 是 skill 生命周期的两阶段，均归 Harness 维护子系统；主张陈述为可证伪命题 P15 而非结果。
2. **新增 §8.2 "From Query Plan to Intermediate Relation"**（§8.1 之后）：把契约映射的 "plan" 步骤实体化为 IR 记录 theme ↦ ⟨{Σ(src)}, 5W1H⟩，六要素（When 时效 / Where 使用范围 / Who 拥有者授权 / What 数据语义 / Why 集成逻辑 / How 物理访问）逐个定义；Data Wiki（数据语义，复杂报表人机协同构建 + reconstructive reflection 校验，P16）与 Theme Wiki（验证收敛的产出模板登记，来自 σ_out 子域）正交，IR 是唯一显式耦合点（P17）；显式声明贡献边界：工程层显式化与重组，非新检索/数据集成算法（引 [2]）。
3. **§9 新增两条评估协议**：9.8 Dual-Subgoal Reward for Skill Training（P15：冻结 SkillOpt 骨架仅改 gate 的对照；收敛编辑数/子域均衡/人工干预次数指标；双维无增益即证伪）与 9.9 Intermediate-Relation Decoupling and Reconstructive Reflection（P16+P17：只换数据源/只换产出格式两类变更的波及范围；N 份人常用报表的还原准确率差距）。
4. **Figure 7 证伪矩阵**：脚本中矩阵表新增两行（Dual-subgoal reward、IR decoupling），caption 更新为九行。
5. **§11 Limitations 改写范围割舍声明**：维护子系统 M 仍超出范围（skill 训练回路与 IR 维护均归属之）；数据子系统 D1–D4 全量形式化与高阶记忆留在配套笔记，本文仅纳入契约相关部分（IR/5W1H 与 Data Wiki / Theme Wiki 分离）。
6. **§2.1 contributions 与 Abstract 同步**：协议清单补两条；次级贡献中 "Skill-as-Code" 扩为 "train-then-freeze Skill lifecycle"。

## v4 — 2026-07-22

审查方式：v3 PDF 全文与 Obsidian vault（`~/Documents/kimi`）原始构想笔记、8 篇精读笔记逐条比对；References 全部 21 条回 arXiv / 官方页面核实。

### References 修正（8 条，全部经 arXiv 官方页核实）

- **[8] ClawVM (2604.10352)**：标题系编造（原 "Deterministic and Auditable Agentic Runtime Harness"）→ 真实标题 *ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents*；作者 "ClawVM Team" 占位 → Mofasshara Rafique, Laurent Bindschaedler。
- **[18] MemGPT (2310.08560)**：作者列表错乱（Wooders 重复、Raganato/Restom-Gonzalez/Narayan 系编造）→ Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez。
- **[19] RAG (Lewis et al. 2020, NeurIPS)**：删除编造的 "Piktus, Vladimir"，修正断词（Küttler、Rocktäschel）；恢复为 Lewis/Perez/A. Piktus/Petroni/Karpukhin/Goyal/Küttler/M. Lewis/Yih/Rocktäschel/Riedel/Kiela。
- **[2] Semantic Metadata (2605.28787)**：第一作者误为 Halevy → 实为 **Shiyu Chen**（Google），作者序 Chen, Alrashed, Halevy, Noy；标题补全 *…A Comparative Study in Agentic Data Retrieval*；正文 "Halevy et al." → "Chen et al."。
- **[15] AgentScope (2402.14034)**：标题误为 "A Comprehensive yet Lightweight…" → *AgentScope: A Flexible yet Robust Multi-Agent Platform*。
- **[16] Agent-as-a-Service (2505.08446)**：标题与 "Team" 作者系编造 → *Agent-as-a-Service based on Agent Network*（AaaS-AN），Yuhan Zhu, Haojie Liu, Jian Wang, Bing Li, Zikang Yin, Yefei Liao。
- **[17] Autellix (2502.13965)**：第一作者误为 "Liu, Xuting" → 实为 **Michael Luo**（UC Berkeley），全作者列表替换；标题补全 *Autellix: An Efficient Serving Engine for LLM Agents as General Programs*。
- **[20] SkillOpt (2605.23904)**：作者占位 "Wang, Yizheng" → 第一作者实为 **Yifan Yang**（Microsoft），补全 15 作者列表。
- 构建脚本 `latex_to_preprint.py` 修复变音符号（`{\"u}`）转义缺陷，消除 "K uttler" 类断词。

### 内容修改

1. §2.1 "four primary contributions" → "five"（实际列 5 条）。
2. §10.1 契约编译延迟（"low tens of milliseconds" 等）缺乏实验依据 → 改为明确假设表述（待 Protocol 9.6 检验，非实测结果）。
3. Table 1 增加表注：评分基于公开文档与引用来源；"This paper" 行标 †，注明为设计目标而非已验证结果。
4. §7.3 机制 2 后新增 Amdahl 参数化短段：Speedup ≤ 1/(s+(1−s)/N)，s = s₀+λρ，E = E₀−μ·c̄；核心命题"并行度上界是工具集切分设计的函数"，声明为待校准设计假设（源自 vault 笔记 `09` P10）。
5. §11 Limitations 新增范围割舍声明：维护/自管理子系统（system skills 归 Harness 治理、走物理轴）与数据子系统完整四组成（on-policy 取数 API、治理即 data-usage skill、生命周期管理）超出本文范围，对应实验协议（数据轴、并行放置、Skill 训练 reward）留待实现阶段。

### 审查中已确认无误、未改动的部分

- 7 篇精读文献（[1][3][4][5][6][7][9][20]）的观点表述与 vault 精读笔记一致。
- Tool Forge "99.2% task-flow tool context reduction" 与精读笔记逐字一致。
- 核心思想谱系（A=⟨S,H,X⟩、条件解耦四假设、CP/DP、KV 前缀冻结四机制、off-policy loop、Skill-as-Code、dry-run、7 条可证伪协议）与 vault 原始笔记保真对应。
