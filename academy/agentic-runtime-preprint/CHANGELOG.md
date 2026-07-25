# CHANGELOG

## v9 — 2026-07-25

审查方式：检索 HuggingFace Daily Papers / arXiv 2026 年 7 月 trending 论文，下载并精读 15 篇直接相关工作（PDF 存于 `academy/papers/pdf/`），据此重划新颖性边界；并把用户口述的 harness 强度设计（子 agent 派生闭包）写入论文。

### 新增内容

1. **新增 §7.4 "Derivation-Closure Orchestration" + Figure 4**：形式化用户的编排设计——子 agent 持有相对固定的 tool-set/data-set 从而界定其输出范围；对集合外工具/数据源的引用不就地授予，而是成为派生下一个子 agent 的准入条件；主 agent 不执行任务工具，只做 summarize + semantic join + top-k，并按声明的 σ_out 子域计算 **satisfaction ratio**（新增公式），据此反复调用/派生子 agent 直至达标、预算耗尽或无候选（后者为 typed failure）。新增 `_draw_derivation_closure` 示意图方法。
2. **§2.1 contributions 第 3 条**扩写以涵盖该编排规则。

### 新颖性边界重划（应对 7 月撞车工作）

- **§4 新增三段**：(a) `soni2026gates` 落地了本文视为设计要求的证伪式 release gate + standing invariants（capability token / control ring、有界模型检查、跨 6 个 release 不变），并实测治理开销 ~0.021ms/请求；明确其范围是单运行时安全核，不涉及逻辑/物理双轴分离。(b) `fan2026skillware` 提供了本文原本隐含的 Skill 软件本体论（Artifact/Unit/Host 三分、lifecycle continuity 可测量、138k 语料），本文采纳其词汇，§8.4 相应收窄。(c) `hsu2026grace` 的 typed graph + 局部邻域验证是 IR 原理的独立证据，区别在于结构化对象不同。另补 `wang2026handbook`/`huang2026memoharness`（归入 §11 已割舍的维护子系统）与 `zhang2026misalignment`/`wang2026skillcorpus`/`badhe2026skillsecurity`（operation closure 的现实障碍与路径安全背景）。
- **§8.5 新增"Relation to concurrent work on structured credit assignment"段**：`luo2026gsme`（按 pathology 索引）与 `lin2026wml`（按 workflow node/mechanism 归因）都按*事后推断的失败属性*索引 credit，本文按*契约先验声明的 σ_out 子域*索引，且与 §7.4 运行期 satisfaction ratio 共用同一结构；明确"契约维度是否优于诊断维度"为开放问题而非主张。引 `wang2026compound`（增益仅在 regression control 内置于优化环时复合）作为前提支持。
- **§8.4 收窄**：把"Skill 值得作为有独立 identity 的软件单元"归给 Skillware，本文只主张 freeze-to-code 阶段与其 release gate。
- **§8.2 P17 补充**：引 GRACE 支持"结构化使验证局部化"，并把 P17 的独特性明确为两个 registry 在单侧变更下的相互独立性。

### 实证依据修正

- **§10.1 删除错误推测**：原文推测契约编译延迟为"low tens of milliseconds"，与 `soni2026gates` 实测 0.021ms 差三个数量级；改为引用该实测值作为下界（其只覆盖不变量求值，不含 schema 校验/图构造/绑定），并明确本文不再自行给出估计，交由 Protocol 9.6 测量。

### 评估协议加固

- **9.1 Control**：新增两项混淆控制——固定并报告 harness 检索能力，且在单源/语料库两个规模下分别测（`he2026disclosure` 发现渐进披露收益在强 harness 下趋零、仅在语料库规模决定性）；激活深度固定为一层（同文献发现第二层从不帮忙、有时降准确率）。
- **9.1 Metrics**：聚合 recall 不足——`xue2026longcontext` 观察到 requirement coverage >92% 而结果崩塌；新增"每条声明需求全满足的运行占比"并记录具体被丢弃的需求。
- **9.7 / 9.8 Control**：采用 executor/grader 分离 + first-attempt grading，self-correction 单独计数而非计入通过（`anand2026aeval` 指出自修复自评会把通过率灌水成虚假 100%）；9.8 另要求过程判据须为运行前登记的固定产物。
- **9.8 Falsification 新增一条**：按 `wang2026phantom` 的反事实设计（该文 60 次运行中 15 次为从未发生的失败类别捏造 guardrail），用 oracle 校验每条 rejection reason；若维度标注理由含 oracle 可反驳的虚构违规，则"归因更清晰"主张失效（即便收敛更快）。
- **§8.5 新增告警段**：r_proc 依赖"step 是否满足判据"的判定，故判据须为登记产物而非评分时由模型生成。

### 引用

- 新增 15 条引用（全部经 arXiv API 官方核实标题与完整作者列表，无占位符/截断）；引用总数 24 → 39。
- 15 篇 PDF 下载至 `academy/papers/pdf/`，沿用既有命名约定 `{arxivID}v{n} {Title}.pdf`。
- **参考文献 PDF 统一归位**：vault 原有的 9 篇参考 PDF 一并移入 `academy/papers/pdf/`（共 24 篇），vault 内 `Papers/PDFs/` 目录移除，另删除 `Workspaces/deep research/` 下两处 18 份重复镜像副本。此后 **vault 只保留本人论文的 PDF 与 md**；vault 内 Notes 与 00_Index 的 PDF 链接改为指向 repo 路径。
- 15 篇已导入 **Zotero**（含 PDF 附件），带 `agentic-runtime` / `2026-07` 及分类标签（高危撞车 / P15平行工作 / 协议警告 等）。

### 渲染 bug 修复（3 处）

- **display equation 从不走数学清理路径**：`code_block()` 直接调 `clean_latex`，而 `clean_latex` 只对 `$...$` 内联公式调用 `clean_math`，导致 `\frac`/`\sum_{}`/`\mapsto`/`\cdot` 在行间公式中全部落空。表现为 `r_proc(s)=1|steps|sum_k ...`（分数塌成并列符号）。现于 `code_block` 内先归一化数学构造再交给 `clean_latex`。
- **`\frac` 完全无处理分支**：新增 `(分子)/(分母)` 转换，正则允许一层嵌套花括号（`\frac{1}{|\mathrm{dom}(\sigma^{out})|}` 需要）。
- **`\sum_{...}` 下标丢失**：新增 `sum over ... of` 转换，同样支持一层嵌套。

### 重建 PDF

- 生成 `output/pdf/..._v9.pdf`（24 页）；全文扫描确认无残留反斜杠/花括号、无词融合、无带空格短横线、无 `Section\d` 断字、无 `sum_`/`frac` 残留、无未解析引用键；Figure 1–8 的 caption 编号与正文引用一致；参考文献 1–39 完整无缺号。

## v8 — 2026-07-25

审查方式：核实用户在其他电脑上完成的 v7 改动（压缩 Abstract、拆分 §8.2/§8.5 段落、新增命题总表、引入 Zep/SoKG/XPEventCore 三条引用、halevy→chen bib key 改名、清理 7 个无用 `_draw_*` 方法），逐条核实新增内容的准确性并修复渲染 bug。

### 引用准确性修正（3 条，全部经 arXiv/HAL 官方页核实）

- **`zep2025`**：作者占位符 "Zep Team" → 实际作者 Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, Daniel Chalef。
- **`sokg2026`**：标题不全（"Knowledge Graph Construction via QA-Driven Fact Extraction"）→ 补全为 *SocraticKG: Knowledge Graph Construction via QA-Driven Fact Extraction*；作者占位符 "SoKG Team" → 实际作者 Sanghyeok Choi, Woosang Jeon, Kyuseok Yang, Taehyeong Kim。
- **`xpeventcore2024`**：作者列表不全（"Piryani, R. and others"）→ 补全五位作者 Rajesh Piryani, Nathalie Aussenac-Gilles, Nathalie Jane Hernandez, Cédric Lopez, Camille Pradel。
- 验证 7 个被删除的 `_draw_*` 方法（`overview`/`stack`/`ontology`/`double_helix`/`architecture_flow`/`results_bar`/`theme_convergence`）确系死代码，未被本论文任何 figure kind 引用，删除无风险。

### 渲染 bug 修复（2 处）

- **`\S` 替换缺空格**：新增命题总表里 `\S5.3`/`\S9.8`/`\S9.9` 渲染为 "Section5.3" 等无空格形式；`re.sub(r"\\S(?![a-zA-Z])", "Section", text)` 缺少尾随空格 → 改为 `"Section "`。
- **法语重音符号 `\'` 未处理**：`Lopez, C{\'e}dric` 渲染为 "C edric"（缺失字母）；脚本此前只处理了变音符 `\"`（如 `K{\"u}ttler`→"Kuttler"），未处理锐音符 `\'`（以及类似的 `` \` ``/`\^`/`\~`/`\=`/`\.`）→ 新增对应正则，与变音符处理一致地去重音為纯 ASCII（"Cédric"→"Cedric"）。

### 重建 PDF

- 生成 `output/pdf/..._v8.pdf`（20 页），全文扫描确认无残留反斜杠/大括号、无相邻宏融合、无带空格短横线、无陈旧占位符作者名。

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
