# v23 Methodological and Threat-Model Revision

日期：2026-08-08

## 修改目标（v22 → v23 聚焦论文）

v23 在 v22（16 页、8 图、focused thesis）基础上补齐审稿必问的四类缺口，不改变中心命题与实验设计。

### A. 威胁模型（审稿必问，正文此前 3 处引用 "the threat model" 却未定义）

- 新增 `\subsection{Threat Model}`（§5 Contract Boundary and Architecture 末尾），压缩 v21 §6.2 的五条威胁模型：trusted computing base / untrusted model output / semi-trusted Skills / untrusted external content / adversary capabilities。
- 收尾明确目标之窄：gates 与 trace 使违规可归因，但不阻止已授权 effect 造成危害。

### B. 记法统一

- 全文 operating region 统一为 `$\Omega$`（正文 "Omega" 全部替换），渲染输出不变（clean_math 将 `\Omega` 渲染为字面 "Omega"），与判决态 "supported within Omega" 一致。

### C. 统计稳健性三补丁

1. **超时截断敏感**：Y_R 端点把超时请求记为 τ 形成点质量；补充 per-cell 超时率报告与备选端点（completed-run p95 / winsorized）敏感性分析要求。
2. **多重性**：六义务各一个单侧 95% 界 + 交互等价 + 语义 NI 需声明 family-wise error 规则（simultaneous coverage 或 predeclared closed testing）。
3. **功效工作样例**：给出 2×2 交叉的最小可检出交互数值示例（σ=0.4 log-p95、ρ=0.05、n=500、k≈41 时 MDI≈0.08 < log(1.10)），并说明更少 cluster 须事先声明 underpowered。

### D. 表达与结构

- Abstract 拆 3 段（problem → hypothesis/mechanism → contribution/evidence status）。
- `two-one-sided-tests rule` → `two one sided tests (TOST)`；m_R 补可读释义（10% 乘法性交互）。
- §4 Related Work 拆 `\paragraph` 块（reference monitors / control architectures / queueing / contemporary）。
- §8 Secondary Protocols 每个命名协议补一行 hypothesis/control/falsification。
- 引用补 goguen1982noninterference，在 §4 把 effect non-interference 落到既有学术谱系。

## 修改目标（v21 → v22 企业论文）

v21 企业白皮书（33 页）为历史锚点，本轮按 16 号笔记"下一轮该做什么"补齐第 1 轮评审未落地项：

- **C1 经典谱系引用**：references.bib 补 anderson1972 / saltzer1975 / parnas1972 / miller2003 / levin1975 / kreutz2015 / kephart2003 / ibm2006 / iso25010 / kleinrock1975 / mars2011 / dean2013 / goguen1982；§4 新增 `\paragraph{Classical foundations.}` 把六条件映射到既有文献——直接回应评审第 3 条与 16 号 §1.2 未决冲突（方案 1）。
- **C2 首次使用展开**：Abstract 中 NFR、CIO 先行展开。
- **C3 capability-count 与 activated behavior 调和**：§9.1 Control 明确 count 轴是 registry-population dose under fixed activation，激活路径构成为行为轴，与 v22/v23 的 treatment 定义一致。
- **C4 Intermediate Relation schema + 端到端 join 示例**（评审第 5 条）。
- **C5 dispute & escalation 小节**（评审第 10 条，"组织即契约"试金石）。
- **C6 形式化边界声明**：§5 一句"notation for the measurement contract, not a formal operational model"（评审第 11 条）。
- **C7 登记 2605.27744 / 2605.28000 为设计动机**（SkillOpt 方式，非证据引用）。

## 版本与产物

- 根论文 `PREPRINT_VERSION` v22 → **v23**，默认产物 `Scalable_Manageable_Agentic_Runtime_Preprint_v23.pdf`；v21/v22 PDF 校验和保持不变。
- separability-study 子项目同步为 v23 内容（`Separability_Study_v23.pdf`）；enterprise-architecture 子项目升为 v22（`Enterprise_Architecture_v22.pdf`）。
- 测试：新增 `test_v23_rendering.py`；`test_v22_rendering.py` 改为读取冻结的 v22 PDF（不再从 live source 构建）。
- sync 后更新 Obsidian vault：00_Index 版本行、16 号评审状态、13/14 号 v23 快照、15 号 v23 复核。

## 验证

1. v23 构建成功，全部渲染测试通过。
2. v21、v22 PDF SHA-256 不变。
3. 提取文本无残留 LaTeX 控制序列、无占位符、无 broken ref。
4. 全文扫描：无 `{`/`}`、无 `??`、无 `the section/the table` 降级回退。
5. 两仓库 `git diff --check` 通过。